from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3, json, re
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB = BASE / 'lld.db'
app = Flask(__name__)
CORS(app)

PROBLEMS = [
    {
        'id': 'parking-lot', 'title': 'Parking Lot', 'difficulty': 'Medium', 'time': '45 min',
        'summary': 'Design a parking lot that supports multiple vehicle types, spot allocation, tickets and fee calculation.',
        'requirements': [
            'Support motorcycle, car and truck vehicles.',
            'Parking spots have compatible spot types and occupancy state.',
            'Issue a ticket when a vehicle is parked and release the spot on exit.',
            'Calculate parking fees based on vehicle type and duration.',
            'Keep allocation, ticketing and pricing responsibilities reasonably separated.'
        ],
        'hints': ['Prefer composition over a large conditional class.', 'Identify the objects that own state and behaviour.', 'Think about how a new vehicle type or pricing rule would be added.']
    },
    {
        'id': 'elevator', 'title': 'Elevator System', 'difficulty': 'Medium', 'time': '45 min',
        'summary': 'Design an elevator system that accepts floor requests and assigns elevators while keeping state and scheduling responsibilities clear.',
        'requirements': [
            'Support multiple elevators and floors.',
            'Handle external hall calls and internal floor requests.',
            'Track elevator state, current floor and direction.',
            'Choose an elevator using a pluggable selection strategy.',
            'Allow a new scheduling strategy without rewriting the elevator domain model.'
        ],
        'hints': ['Separate request selection from elevator state.', 'A strategy interface can keep scheduling extensible.', 'Avoid putting every responsibility in ElevatorSystem.']
    },
    {
        'id': 'vending-machine', 'title': 'Vending Machine', 'difficulty': 'Easy', 'time': '30 min',
        'summary': 'Design a vending machine with inventory, product selection, payment and change handling.',
        'requirements': [
            'Maintain product inventory and prices.',
            'Allow a customer to select an available product.',
            'Accept a payment and validate the amount.',
            'Return change and dispense the selected product.',
            'Handle cancelled purchases and out-of-stock products safely.'
        ],
        'hints': ['Model machine state explicitly.', 'Keep inventory and payment concerns separate.', 'Consider how the flow changes after payment is accepted.']
    }
]


def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = db()
    con.execute('''CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id TEXT NOT NULL,
        solution TEXT NOT NULL,
        feedback TEXT NOT NULL,
        score INTEGER NOT NULL,
        created_at TEXT NOT NULL
    )''')
    con.commit(); con.close()


def evaluate(problem, solution):
    text = solution.strip()
    lower = text.lower()
    words = len(re.findall(r'\b\w+\b', text))
    signals = {
        'classes': bool(re.search(r'\b(class|interface|object|entity|model)\b', lower)),
        'responsibility': bool(re.search(r'\b(responsibilit|single responsibility|srp|separation of concern)\w*\b', lower)),
        'relationship': bool(re.search(r'\b(association|composition|aggregation|inheritance|dependency|relationship)\w*\b', lower)),
        'extensibility': bool(re.search(r'\b(strategy|factory|interface|extensib|open.?closed|new vehicle|new pricing|new scheduling)\w*\b', lower)),
        'edge': bool(re.search(r'\b(edge|error|invalid|empty|full|unavailable|out.?of.?stock|cancel|failure|capacity)\w*\b', lower)),
        'tradeoff': bool(re.search(r'\b(trade.?off|tradeoff|simpler|complexity|scalab|alternative)\w*\b', lower)),
    }
    score = 30
    score += 12 if signals['classes'] else 0
    score += 12 if signals['responsibility'] else 0
    score += 12 if signals['relationship'] else 0
    score += 12 if signals['extensibility'] else 0
    score += 10 if signals['edge'] else 0
    score += 8 if signals['tradeoff'] else 0
    score += 4 if words >= 120 else 0
    score = min(score, 100)
    positives, improvements = [], []
    if signals['classes']: positives.append('You identified domain objects/classes instead of describing only a high-level workflow.')
    else: improvements.append('Name the key domain classes/interfaces and briefly state what each owns.')
    if signals['responsibility']: positives.append('You addressed responsibility boundaries, which is important for maintainable LLD.')
    else: improvements.append('Explain which class owns each responsibility and avoid a single “god” service.')
    if signals['relationship']: positives.append('You discussed relationships between objects.')
    else: improvements.append('Make relationships explicit: composition, association, dependency, or inheritance where appropriate.')
    if signals['extensibility']: positives.append('You considered an extension point such as a strategy or interface.')
    else: improvements.append('Show one likely change and how your design accommodates it without rewriting core classes.')
    if signals['edge']: positives.append('You considered failure or edge cases.')
    else: improvements.append('Add at least two edge cases and define expected behaviour.')
    if signals['tradeoff']: positives.append('You documented a design trade-off rather than presenting one solution as universally correct.')
    else: improvements.append('State one trade-off: what your design simplifies and what complexity it introduces.')
    if words < 80: improvements.append('The attempt is quite short; add a compact class list and a request/flow example.')
    return {
        'score': score,
        'summary': 'This feedback uses transparent, rule-based checks for the MVP. Multiple valid designs can still exist; the score is a guide, not a claim that one LLD is the only correct solution.',
        'strengths': positives[:4],
        'improvements': improvements[:5],
        'signals': signals,
        'next_step': 'Revise the design using the improvement points, then submit another attempt.'
    }


@app.get('/api/health')
def health(): return jsonify({'ok': True})

@app.get('/api/problems')
def problems(): return jsonify(PROBLEMS)

@app.get('/api/problems/<pid>')
def problem(pid):
    p = next((x for x in PROBLEMS if x['id'] == pid), None)
    return (jsonify(p), 200) if p else (jsonify({'error':'Problem not found'}), 404)

@app.post('/api/attempts')
def submit():
    data = request.get_json(silent=True) or {}
    pid = data.get('problem_id'); solution = (data.get('solution') or '').strip()
    p = next((x for x in PROBLEMS if x['id'] == pid), None)
    if not p: return jsonify({'error':'Problem not found'}), 404
    if len(solution) < 30: return jsonify({'error':'Please submit at least 30 characters so the design can be evaluated.'}), 400
    feedback = evaluate(p, solution)
    now = datetime.utcnow().isoformat(timespec='seconds') + 'Z'
    con = db()
    cur = con.execute('INSERT INTO attempts(problem_id,solution,feedback,score,created_at) VALUES (?,?,?,?,?)', (pid, solution, json.dumps(feedback), feedback['score'], now))
    con.commit(); attempt_id = cur.lastrowid; con.close()
    return jsonify({'id':attempt_id, 'problem':p, 'solution':solution, 'feedback':feedback, 'created_at':now})

@app.get('/api/attempts')
def attempts():
    con = db(); rows = con.execute('SELECT * FROM attempts ORDER BY id DESC').fetchall(); con.close()
    out=[]
    for r in rows:
        out.append({'id':r['id'],'problem_id':r['problem_id'],'score':r['score'],'created_at':r['created_at'],'feedback':json.loads(r['feedback']),'solution':r['solution']})
    return jsonify(out)

@app.get('/api/attempts/<int:aid>')
def attempt(aid):
    con=db(); r=con.execute('SELECT * FROM attempts WHERE id=?',(aid,)).fetchone(); con.close()
    if not r: return jsonify({'error':'Attempt not found'}),404
    return jsonify({'id':r['id'],'problem_id':r['problem_id'],'score':r['score'],'created_at':r['created_at'],'feedback':json.loads(r['feedback']),'solution':r['solution']})

if __name__ == '__main__':
    init_db(); app.run(host='0.0.0.0', port=5000, debug=True)
