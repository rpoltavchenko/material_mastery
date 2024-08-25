from app import db

class MaterialCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    properties = db.Column(db.Text, nullable=False)
    uses = db.Column(db.Text, nullable=False)

class ChallengeCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    key_considerations = db.Column(db.Text, nullable=True)
    bonus_points = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<ChallengeCard {self.title}>'
                

class BonusCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    effect = db.Column(db.Text, nullable=False)
    scoring_rules = db.Column(db.Text, nullable=False)

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    number_of_rounds = db.Column(db.Integer, nullable=False)
    current_round = db.Column(db.Integer, default=1)
    teams = db.relationship('Team', backref='game_session', lazy=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    rounds = db.relationship('Round', backref='game_session', lazy=True)

class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(db.Integer, nullable=False)
    game_session_id = db.Column(db.Integer, db.ForeignKey('game_session.id'))
    challenge_card_id = db.Column(db.Integer, db.ForeignKey('ChallengeCard.id'))
    bonus_card_id = db.Column(db.Integer, db.ForeignKey('BonusCard.id'))


class DesignSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('Team.id'))
    round_id = db.Column(db.Integer, db.ForeignKey('Round.id'))
    design_data = db.Column(db.Text, nullable=False)  # Could store JSON or any design-related data
    score = db.Column(db.Integer, nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    game_session_id = db.Column(db.Integer, db.ForeignKey('game_session.id'))
    users = db.relationship('User', backref='team', lazy=True)

    def add_user(self, user):
        if len(self.users) < 5:
            self.users.append(user)
        else:
            raise ValueError("Team cannot have more than 5 users.")
