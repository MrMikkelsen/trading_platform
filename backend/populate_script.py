from DB.models.securities import Security
from DB.models.team import Team
from DB.models.goodwill import Goodwill
from utils.exchange import prices_con
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

TEAM_NAMES = ["Gaussian Gamblerz", "Code@LTH", "Lunds Luringar", "Epsilon", "AlgoDator", "DMCG", "Parentesen IG", "Algo-rhythmics", "ByteBard", "Wimialto"]

def populate_with_dummy_data():
    engine = create_engine(
        'postgresql://stock:D3nt15t_@postgrelinc.postgres.database.azure.com:5432/postgres')

    Session = scoped_session(sessionmaker(bind=engine))
    # populate with dummy data
    with Session() as session:
        # if team is not empty, populate with dummy data
        if session.query(Team).count() == 0:
            admin = Team(name="Admin", role="admin", saldo=0, starting_saldo=0)
            session.add(admin)
            for i in range(len(TEAM_NAMES)):
                team = Team(name=f"Team {TEAM_NAMES[i]}", role="group",
                            saldo=100000, starting_saldo=100000)
                session.add(team)
            session.commit()

        # if stock is not empty, populate with dummy data
        if session.query(Security).count() == 0:
            all_stocks = prices_con.get_all_symbols()
            for stock in all_stocks:
                session.add(Security(security_type='stock', symbol=stock))
            session.commit()


def main():
    populate_with_dummy_data()


if __name__ == "__main__":
    main()
