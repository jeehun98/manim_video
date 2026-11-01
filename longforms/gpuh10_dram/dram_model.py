class BankModel:
    """One simplified bank, at most one active row; no real-device address mapping/timing."""
    def __init__(self,active=None):self.active=active
    def read(self,row,col):
        assert 0<=row<4 and 0<=col<8
        before=self.active
        commands=(['ACTIVATE','READ'] if before is None else ['READ'] if before==row else ['PRECHARGE','ACTIVATE','READ'])
        self.active=row
        return dict(bank=0,row=row,col=col,before=before,after=row,commands=commands,value={(1,2):6,(1,5):9,(3,2):26}.get((row,col),0),conceptual=True)
