from src.models.user_models import BaseModel, db
import pandas as pd


class Strains(BaseModel):
    __tablename__ = 'strains'

    id = db.Column(db.Integer(), primary_key=True)
    strain = db.Column(db.String())
    type = db.Column(db.String())
    rating = db.Column(db.REAL())
    effects = db.Column(db.String())
    flavor = db.Column(db.String())
    description = db.Column(db.String())


file_name = "../static/data/cannabis.csv"

# df = pd.read_csv(file_name)
