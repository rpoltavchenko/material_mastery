from flask import Blueprint, jsonify, request

from app import db
from app.models import MaterialCard
from app.models import ChallengeCard
from app.models import Team, User


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return "<h1>Welcome to Material Mastery!</h1>"

@bp.route('/material-cards', methods=['GET'])
def get_material_cards():
    cards = MaterialCard.query.all()
    return jsonify([card.name for card in cards])

@bp.route('/material-cards', methods=['POST'])
def add_material_card():
    data = request.get_json()
    new_card = MaterialCard(name=data['name'], properties=data['properties'], uses=data['uses'])
    db.session.add(new_card)
    db.session.commit()
    return jsonify({'message': 'Material card added successfully!'}), 201

@bp.route('/material-cards/<int:id>', methods=['PUT'])
def update_material_card(id):
    data = request.get_json()
    
    # Fetch the material card by ID
    material_card = MaterialCard.query.get_or_404(id)
    
    # Validate input data and update fields
    if 'name' in data:
        material_card.name = data['name']
    if 'properties' in data:
        material_card.properties = data['properties']
    if 'uses' in data:
        material_card.uses = data['uses']
    
    # Commit the changes to the database
    try:
        db.session.commit()
        return jsonify({'message': 'Material card updated successfully!', 'material_card': {
            'id': material_card.id,
            'name': material_card.name,
            'properties': material_card.properties,
            'uses': material_card.uses
        }}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/material-cards/<int:id>', methods=['DELETE'])
def delete_material_card(id):
    # Fetch the material card by ID
    material_card = MaterialCard.query.get_or_404(id)

    try:
        # Delete the material card from the database
        db.session.delete(material_card)
        db.session.commit()
        return jsonify({'message': f'Material card with ID {id} deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# app/routes.py

@bp.route('/challenge-cards', methods=['GET'])
def get_challenge_cards():
    # Query all challenge cards from the database
    challenge_cards = ChallengeCard.query.all()
    
    # Serialize the challenge cards into a list of dictionaries
    result = []
    for card in challenge_cards:
        card_data = {
            'id': card.id,
            'title': card.title,
            'description': card.description,
            'key_considerations': card.key_considerations,
            'bonus_points': card.bonus_points
        }
        result.append(card_data)
    
    # Return the serialized list as a JSON response
    return jsonify(result), 200

@bp.route('/challenge-cards', methods=['POST'])
def create_challenge_card():
    data = request.get_json()

    # Validate input data
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    if not data.get('description'):
        return jsonify({'error': 'Description is required'}), 400

    # Create a new ChallengeCard instance
    new_card = ChallengeCard(
        title=data['title'],
        description=data['description'],
        key_considerations=data.get('key_considerations'),
        bonus_points=data.get('bonus_points')
    )

    # Add to the database and commit
    try:
        db.session.add(new_card)
        db.session.commit()
        return jsonify({'message': 'Challenge card created successfully!', 'id': new_card.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/challenge-cards/<int:id>', methods=['PUT'])
def update_challenge_card(id):
    # Fetch the existing challenge card by ID
    challenge_card = ChallengeCard.query.get_or_404(id)

    # Parse the request data
    data = request.get_json()

    # Update the challenge card's attributes
    if 'title' in data:
        challenge_card.title = data['title']
    if 'description' in data:
        challenge_card.description = data['description']
    if 'requirements' in data:
        challenge_card.requirements = data['requirements']

    # Save the changes to the database
    try:
        db.session.commit()
        return jsonify({
            'message': 'Challenge card updated successfully!',
            'challenge_card': {
                'id': challenge_card.id,
                'title': challenge_card.title,
                'description': challenge_card.description,
                'requirements': challenge_card.requirements
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

bp = Blueprint('main', __name__)

@bp.route('/challenge-cards/<int:id>', methods=['DELETE'])
def delete_challenge_card(id):
    # Find the challenge card by ID
    challenge_card = ChallengeCard.query.get_or_404(id)

    # Delete the challenge card
    db.session.delete(challenge_card)

    # Commit the change to the database
    try:
        db.session.commit()
        return jsonify({'message': f'Challenge card {id} deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/bonus-cards', methods=['GET'])
def get_bonus_cards():
    bonus_cards = BonusCard.query.all()
    return jsonify([{
        'id': card.id,
        'name': card.name,
        'effect': card.effect,
        'scoring_rules': card.scoring_rules
    } for card in bonus_cards])


@bp.route('/bonus-cards/<int:id>', methods=['PUT'])
def update_bonus_card(id):
    # Find the bonus card by ID
    bonus_card = BonusCard.query.get_or_404(id)

    # Parse the request data
    data = request.get_json()

    # Update the bonus card's attributes
    if 'name' in data:
        bonus_card.name = data['name']
    if 'effect' in data:
        bonus_card.effect = data['effect']
    if 'scoring_rules' in data:
        bonus_card.scoring_rules = data['scoring_rules']

    # Save the changes to the database
    try:
        db.session.commit()
        return jsonify({
            'message': 'Bonus card updated successfully!',
            'bonus_card': {
                'id': bonus_card.id,
                'name': bonus_card.name,
                'effect': bonus_card.effect,
                'scoring_rules': bonus_card.scoring_rules
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/bonus-cards', methods=['POST'])
def add_bonus_card():
    # Parse the request data
    data = request.get_json()

    # Validate input
    if not data.get('name') or not data.get('effect') or not data.get('scoring_rules'):
        return jsonify({'error': 'Name, effect, and scoring rules are required fields.'}), 400

    # Create a new BonusCard object
    new_card = BonusCard(
        name=data['name'],
        effect=data['effect'],
        scoring_rules=data['scoring_rules']
    )

    # Add the new card to the database
    try:
        db.session.add(new_card)
        db.session.commit()
        return jsonify({
            'message': 'Bonus card added successfully!',
            'bonus_card': {
                'id': new_card.id,
                'name': new_card.name,
                'effect': new_card.effect,
                'scoring_rules': new_card.scoring_rules
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/bonus-cards/<int:id>', methods=['DELETE'])
def delete_bonus_card(id):
    # Find the bonus card by ID
    bonus_card = BonusCard.query.get_or_404(id)

    # Delete the bonus card
    db.session.delete(bonus_card)

    # Commit the change to the database
    try:
        db.session.commit()
        return jsonify({'message': f'Bonus card {id} deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/game-sessions', methods=['POST'])
def create_game_session():
    # Parse the request data
    data = request.get_json()

    # Validate input
    if not data.get('name') or not data.get('number_of_rounds') or not data.get('teams'):
        return jsonify({'error': 'Name, number of rounds, and teams are required fields.'}), 400

    # Create a new GameSession object
    new_session = GameSession(
        name=data['name'],
        number_of_rounds=data['number_of_rounds']
    )

    # Add teams to the session
    for team_data in data['teams']:
        if 'name' in team_data:
            team = Team(name=team_data['name'])
            new_session.teams.append(team)

    # Add the new session to the database
    try:
        db.session.add(new_session)
        db.session.commit()
        return jsonify({
            'message': 'Game session created successfully!',
            'game_session': {
                'id': new_session.id,
                'name': new_session.name,
                'number_of_rounds': new_session.number_of_rounds,
                'current_round': new_session.current_round,
                'teams': [{'id': team.id, 'name': team.name} for team in new_session.teams]
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

bp = Blueprint('main', __name__)

@bp.route('/game-sessions/<int:id>', methods=['GET'])
def get_game_session(id):
    # Find the game session by ID
    game_session = GameSession.query.get_or_404(id)

    # Prepare the response data
    response = {
        'id': game_session.id,
        'name': game_session.name,
        'number_of_rounds': game_session.number_of_rounds,
        'current_round': game_session.current_round,
        'teams': [{'id': team.id, 'name': team.name} for team in game_session.teams],
        'cards_in_play': [{'id': card.id, 'type': card.type, 'description': card.description} for card in game_session.cards_in_play]
    }

    return jsonify(response), 200

@bp.route('/game-sessions/<int:id>', methods=['PUT'])
def update_game_session(id):
    # Find the game session by ID
    game_session = GameSession.query.get_or_404(id)

    # Parse the request data
    data = request.get_json()

    # Update the current round
    if 'current_round' in data:
        new_round = data['current_round']
        if 1 <= new_round <= game_session.number_of_rounds:
            game_session.current_round = new_round
        else:
            return jsonify({'error': 'Invalid round number.'}), 400

    # Update team scores
    if 'teams' in data:
        for team_data in data['teams']:
            team = Team.query.filter_by(id=team_data['id'], game_session_id=game_session.id).first()
            if team:
                team.score = team_data.get('score', team.score)

    # Save the changes to the database
    try:
        db.session.commit()
        return jsonify({
            'message': 'Game session updated successfully!',
            'game_session': {
                'id': game_session.id,
                'name': game_session.name,
                'current_round': game_session.current_round,
                'teams': [{'id': team.id, 'name': team.name, 'score': team.score} for team in game_session.teams]
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/game-sessions/<int:id>', methods=['DELETE'])
def delete_game_session(id):
    # Find the game session by ID
    game_session = GameSession.query.get_or_404(id)

    # Delete the game session
    db.session.delete(game_session)

    # Commit the changes to the database
    try:
        db.session.commit()
        return jsonify({'message': f'Game session {id} deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/game-sessions/<int:id>/start-round', methods=['POST'])
def start_round(id):
    # Find the game session by ID
    game_session = GameSession.query.get_or_404(id)

    # Ensure there are rounds remaining
    if game_session.current_round >= game_session.number_of_rounds:
        return jsonify({'error': 'All rounds have already been completed.'}), 400

    # Increment the round number
    game_session.current_round += 1

    # Draw a random challenge card
    challenge_card = ChallengeCard.query.order_by(db.func.random()).first()
    if not challenge_card:
        return jsonify({'error': 'No challenge cards available.'}), 400

    # Draw a random bonus card
    bonus_card = BonusCard.query.order_by(db.func.random()).first()
    if not bonus_card:
        return jsonify({'error': 'No bonus cards available.'}), 400

    # Create the new round
    new_round = Round(
        round_number=game_session.current_round,
        game_session_id=game_session.id,
        challenge_card_id=challenge_card.id,
        bonus_card_id=bonus_card.id
    )
    db.session.add(new_round)

    # Save the changes to the database
    try:
        db.session.commit()
        return jsonify({
            'message': 'New round started successfully!',
            'round': {
                'round_number': new_round.round_number,
                'challenge_card': {
                    'id': challenge_card.id,
                    'title': challenge_card.title,
                    'description': challenge_card.description
                },
                'bonus_card': {
                    'id': bonus_card.id,
                    'name': bonus_card.name,
                    'effect': bonus_card.effect,
                    'scoring_rules': bonus_card.scoring_rules
                }
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/game-sessions/<int:id>/submit-design', methods=['PUT'])
def submit_design(id):
    # Find the game session by ID
    game_session = GameSession.query.get_or_404(id)

    # Ensure the current round is valid
    if game_session.current_round > game_session.number_of_rounds:
        return jsonify({'error': 'No active round in progress.'}), 400

    # Get the current round
    current_round = Round.query.filter_by(game_session_id=id, round_number=game_session.current_round).first()
    if not current_round:
        return jsonify({'error': 'Current round not found.'}), 404

    # Parse the request data
    data = request.get_json()
    team_id = data.get('team_id')
    design_data = data.get('design_data')

    # Validate input
    if not team_id or not design_data:
        return jsonify({'error': 'Team ID and design data are required.'}), 400

    # Find the team
    team = Team.query.filter_by(id=team_id, game_session_id=game_session.id).first()
    if not team:
        return jsonify({'error': 'Team not found.'}), 404

    # Check if the team already submitted a design for this round
    existing_submission = DesignSubmission.query.filter_by(team_id=team.id, round_id=current_round.id).first()
    if existing_submission:
        return jsonify({'error': 'Design already submitted for this round.'}), 400

    # Create a new design submission
    submission = DesignSubmission(
        team_id=team.id,
        round_id=current_round.id,
        design_data=design_data
    )
    db.session.add(submission)

    # Save the changes to the database
    try:
        db.session.commit()
        return jsonify({
            'message': 'Design submitted successfully!',
            'submission': {
                'id': submission.id,
                'team_id': submission.team_id,
                'round_id': submission.round_id,
                'design_data': submission.design_data
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/game-sessions/<int:id>/round-results', methods=['GET'])
def get_round_results(id):
    # Find the game session by ID
    game_session = GameSession.query.get_or_404(id)

    # Get the current round
    current_round = Round.query.filter_by(game_session_id=id, round_number=game_session.current_round).first()
    if not current_round:
        return jsonify({'error': 'Current round not found or not yet started.'}), 404

    # Get all design submissions for the current round
    submissions = DesignSubmission.query.filter_by(round_id=current_round.id).all()

    # Prepare the results
    results = []
    for submission in submissions:
        results.append({
            'team_id': submission.team_id,
            'design_data': submission.design_data,
            'score': submission.score
        })

    return jsonify({
        'round_number': current_round.round_number,
        'results': results
    }), 200       

@bp.route('/game-sessions/<int:id>/score-round', methods=['POST'])
def score_round(id):
    # Find the game session by ID
    game_session = GameSession.query.get_or_404(id)

    # Get the current round
    current_round = Round.query.filter_by(game_session_id=id, round_number=game_session.current_round).first()
    if not current_round:
        return jsonify({'error': 'Current round not found or not yet started.'}), 404

    # Get all design submissions for the current round
    submissions = DesignSubmission.query.filter_by(round_id=current_round.id).all()

    if not submissions:
        return jsonify({'error': 'No submissions found for this round.'}), 400

    # Calculate the scores
    for submission in submissions:
        # Implement your scoring logic here
        # For example, you might calculate scores based on material selection, creativity, etc.
        material_score = 50  # Placeholder value
        creativity_score = 30  # Placeholder value
        total_score = material_score + creativity_score

        # Update the submission with the calculated score
        submission.score = total_score

        # Update the team's total score
        team = Team.query.get(submission.team_id)
        team.score += total_score

    # Save the changes to the database
    try:
        db.session.commit()
        return jsonify({
            'message': 'Round scored successfully!',
            'round_number': current_round.round_number,
            'results': [
                {
                    'team_id': submission.team_id,
                    'design_data': submission.design_data,
                    'score': submission.score
                } for submission in submissions
            ]
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/leaderboards', methods=['GET'])
def get_leaderboards():
    # Query the top teams sorted by score in descending order
    top_teams = Team.query.order_by(Team.score.desc()).all()

    # Prepare the leaderboard data
    leaderboard = [{
        'team_id': team.id,
        'team_name': team.name,
        'score': team.score
    } for team in top_teams]

    return jsonify({
        'leaderboard': leaderboard
    }), 200
     

@bp.route('/teams', methods=['POST'])
def create_team():
    data = request.get_json()
    
    # Check if team name is provided
    if 'name' not in data or not data['name']:
        return jsonify({'error': 'Team name is required'}), 400

    # Check if users are provided
    if 'users' not in data or len(data['users']) == 0:
        return jsonify({'error': 'At least one user is required to create a team'}), 400

    # Check if more than 5 users are provided
    if len(data['users']) > 5:
        return jsonify({'error': 'A team cannot have more than 5 users'}), 400

    # Check if the team name already exists
    existing_team = Team.query.filter_by(name=data['name']).first()
    if existing_team:
        return jsonify({'error': 'Team name already exists'}), 400

    # Create a new team
    team = Team(name=data['name'])
    db.session.add(team)

    # Add users to the team
    for user_data in data['users']:
        user = User.query.filter_by(email=user_data['email']).first()
        if not user:
            user = User(username=user_data['username'], email=user_data['email'])
            db.session.add(user)
        team.add_user(user)

    # Commit the changes to the database
    try:
        db.session.commit()
        return jsonify({'message': 'Team created successfully!', 'team': team.name, 'users': [user.email for user in team.users]}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/teams', methods=['GET'])
def get_all_teams():
    teams = Team.query.all()
    teams_list = []
    
    for team in teams:
        team_data = {
            'id': team.id,
            'name': team.name,
            'users': [{'id': user.id, 'username': user.username, 'email': user.email} for user in team.users]
        }
        teams_list.append(team_data)

    return jsonify(teams_list), 200
