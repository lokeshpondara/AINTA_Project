# Fix AINTA System Issues from Logs

Status: In Progress

## Current Issues:
- Email alerts fail: KeyError 'smtp_user' 
- GNN model warning (though files exist)
- Sklearn pickle version warnings

## Steps:
1. [ ] Edit config.yaml: Add `smtp_user: aintaproject@gmail.com` under response:
2. [ ] Edit requirements.txt: Change `scikit-learn` to `scikit-learn==1.7.1`
3. [ ] Run `pip install -r requirements.txt`
4. [ ] Test: `python run_system.py` - check no email error, emails send, GNN loads, no warnings
5. [ ] Debug GNN if still fails
6. [ ] Mark complete

**Next Step:** Implementing Step 1
