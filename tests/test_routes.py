import unittest
from app import create_app, db
from app.models import MaterialCard

class MaterialCardTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_material_cards(self):
        response = self.client.get('/material-cards')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

def test_create_team(self):
    response = self.client.post('/teams', json={
        "name": "Team Alpha",
        "users": [
            {"username": "user1", "email": "user1@example.com"},
            {"username": "user2", "email": "user2@example.com"}
        ]
    })
    self.assertEqual(response.status_code, 201)
    self.assertIn('Team created successfully!', str(response.data))

    # Test for team name required
    response = self.client.post('/teams', json={
        "users": [
            {"username": "user1", "email": "user1@example.com"},
            {"username": "user2", "email": "user2@example.com"}
        ]
    })
    self.assertEqual(response.status_code, 400)
    self.assertIn('Team name is required', str(response.data))

    # Test for user limit
    response = self.client.post('/teams', json={
        "name": "Team Beta",
        "users": [
            {"username": "user1", "email": "user1@example.com"},
            {"username": "user2", "email": "user2@example.com"},
            {"username": "user3", "email": "user3@example.com"},
            {"username": "user4", "email": "user4@example.com"},
            {"username": "user5", "email": "user5@example.com"},
            {"username": "user6", "email": "user6@example.com"}
        ]
    })
    self.assertEqual(response.status_code, 400)
    self.assertIn('A team cannot have more than 5 users', str(response.data))

def test_get_all_teams(self):
    # Create a couple of teams for testing
    team1 = Team(name='Team Alpha')
    team2 = Team(name='Team Beta')
    user1 = User(username='user1', email='user1@example.com', team=team1)
    user2 = User(username='user2', email='user2@example.com', team=team1)
    user3 = User(username='user3', email='user3@example.com', team=team2)
    user4 = User(username='user4', email='user4@example.com', team=team2)

    db.session.add_all([team1, team2, user1, user2, user3, user4])
    db.session.commit()

    response = self.client.get('/teams')
    self.assertEqual(response.status_code, 200)
    data = response.get_json()

    # Verify the response data structure
    self.assertEqual(len(data), 2)
    self.assertEqual(data[0]['name'], 'Team Alpha')
    self.assertEqual(len(data[0]['users']), 2)
    self.assertEqual(data[1]['name'], 'Team Beta')
    self.assertEqual(len(data[1]['users']), 2)

def test_update_material_card(self):
    # Create a material card for testing
    material_card = MaterialCard(name='Concrete', properties='High strength', uses='Buildings')
    db.session.add(material_card)
    db.session.commit()

    # Update the material card
    response = self.client.put(f'/material-cards/{material_card.id}', json={
        "name": "Updated Concrete",
        "properties": "Improved compressive strength, better durability",
        "uses": "Foundations, high-rise buildings"
    })
    self.assertEqual(response.status_code, 200)
    self.assertIn('Material card updated successfully!', str(response.data))

    # Verify the updated values
    updated_material_card = MaterialCard.query.get(material_card.id)
    self.assertEqual(updated_material_card.name, "Updated Concrete")
    self.assertEqual(updated_material_card.properties, "Improved compressive strength, better durability")
    self.assertEqual(updated_material_card.uses, "Foundations, high-rise buildings")


def test_delete_material_card(self):
    # Create a material card for testing
    material_card = MaterialCard(name='Concrete', properties='High strength', uses='Buildings')
    db.session.add(material_card)
    db.session.commit()

    # Delete the material card
    response = self.client.delete(f'/material-cards/{material_card.id}')
    self.assertEqual(response.status_code, 200)
    self.assertIn(f'Material card with ID {material_card.id} deleted successfully!', str(response.data))

    # Verify the material card has been deleted
    deleted_material_card = MaterialCard.query.get(material_card.id)
    self.assertIsNone(deleted_material_card)


def test_get_challenge_cards(self):
    # Add a couple of challenge cards for testing
    card1 = ChallengeCard(
        title="Design a Sustainable Home in a Cold Climate",
        description="Create a design for a residential home that prioritizes energy efficiency and sustainability in a cold climate.",
        key_considerations="Thermal insulation, renewable materials, energy-efficient windows, structural integrity under snow load.",
        bonus_points=10
    )
    card2 = ChallengeCard(
        title="Create a High-Rise Office Building with Maximum Transparency",
        description="Design a modern office building that maximizes natural light and offers panoramic views of the city.",
        key_considerations="Structural support for large glass facades, thermal efficiency, glare reduction, aesthetic appeal.",
        bonus_points=15
    )
    
    db.session.add_all([card1, card2])
    db.session.commit()

    # Send GET request
    response = self.client.get('/challenge-cards')
    self.assertEqual(response.status_code, 200)
    data = response.get_json()

    # Verify the response data structure
    self.assertEqual(len(data), 2)
    self.assertEqual(data[0]['title'], 'Design a Sustainable Home in a Cold Climate')
    self.assertEqual(data[1]['title'], 'Create a High-Rise Office Building with Maximum Transparency')


def test_create_challenge_card(self):
    response = self.client.post('/challenge-cards', json={
        "title": "Design a Pavilion for a Tropical Environment",
        "description": "Create a pavilion that is well-suited for a hot and humid tropical climate, focusing on natural ventilation and protection from the elements.",
        "key_considerations": "Weather-resistant materials, shading, cross-ventilation, lightweight construction.",
        "bonus_points": 8
    })
    self.assertEqual(response.status_code, 201)
    self.assertIn('Challenge card created successfully!', str(response.data))

    # Verify the challenge card was added to the database
    card = ChallengeCard.query.filter_by(title="Design a Pavilion for a Tropical Environment").first()
    self.assertIsNotNone(card)
    self.assertEqual(card.description, "Create a pavilion that is well-suited for a hot and humid tropical climate, focusing on natural ventilation and protection from the elements.")
    self.assertEqual(card.key_considerations, "Weather-resistant materials, shading, cross-ventilation, lightweight construction.")
    self.assertEqual(card.bonus_points, 8)
