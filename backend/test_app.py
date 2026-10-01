import json, tempfile, os
import app

app.app.config['TESTING']=True

# Unit tests for the important evaluator behaviour.
def test_evaluator_rewards_design_signals():
    p=app.PROBLEMS[0]
    text='''class ParkingLot owns spots. ParkingTicket stores entry time. Vehicle is an interface. PricingStrategy calculates fees. ParkingLot composes spots and delegates pricing. If the lot is full, reject parking. Trade-off: strategy adds classes but makes pricing extensible.'''
    result=app.evaluate(p,text)
    assert result['score'] >= 80
    assert result['signals']['classes']
    assert result['signals']['extensibility']

def test_short_submission_is_not_accepted_by_api():
    with tempfile.TemporaryDirectory() as d:
        old=app.DB; app.DB=os.path.join(d,'test.db'); app.init_db()
        client=app.app.test_client()
        r=client.post('/api/attempts',json={'problem_id':'parking-lot','solution':'too short'})
        assert r.status_code == 400
        app.DB=old
