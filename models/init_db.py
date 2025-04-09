from models import db, ExchangeRate

def initialize():
    db.connect()
    db.create_tables([ExchangeRate], safe=True)
    db.close()

if __name__ == "__main__":
    initialize()
