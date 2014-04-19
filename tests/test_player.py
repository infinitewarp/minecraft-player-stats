import os

from mock import patch

from mcstats.player import Player


@patch.object(Player, '_fetch_profile')
def test_achievements(mock_fetch_profile):
    mock_fetch_profile.return_value = None

    player = Player(None)
    player._load_stat('achievement.killEnemy', 769)
    player._load_stat('achievement.buildWorkBench', 4)
    player._load_stat('achievement.mineWood', 2271)
    player._load_stat('achievement.exploreAllBiomes', {'value': 0})
    assert player.achievements == ['Benchmarking', 'Getting Wood', 'Monster Hunter']

    player = Player(None)
    player._load_stat('achievement.exploreAllBiomes', {'value': 1})
    assert player.achievements == ['Adventuring Time']


@patch.object(Player, '_fetch_profile')
def test_kills(mock_fetch_profile):
    mock_fetch_profile.return_value = None

    player = Player(None)
    player._load_stat('stat.killEntity.Cow', 5)
    player._load_stat('stat.killEntity.Pig', 23)
    player._load_stat('stat.killEntity.Sheep', 21)
    assert player.kills == [('Pig', 23), ('Sheep', 21), ('Cow', 5)]


@patch.object(Player, '_fetch_profile')
def test_killed_by(mock_fetch_profile):
    mock_fetch_profile.return_value = None

    player = Player(None)
    player._load_stat('stat.entityKilledBy.Creeper', 5)
    player._load_stat('stat.entityKilledBy.Skeleton', 23)
    player._load_stat('stat.entityKilledBy.Zombie', 21)
    assert player.killed_by == [('Skeleton', 23), ('Zombie', 21), ('Creeper', 5)]


@patch.object(Player, '_fetch_profile')
def test_extract_filename(mock_fetch_profile):
    mock_fetch_profile.return_value = None

    player = Player(None)
    filepath = os.path.join('stats', 'notch.json')
    name, is_uuid = player._extract_filename(filepath)
    assert name == 'notch'
    assert is_uuid is False

    player = Player(None)
    filepath = os.path.join('stats', '069a79f4-44e9-4726-a5be-fca90e38aaf5.json')
    name, is_uuid = player._extract_filename(filepath)
    assert name == '069a79f444e94726a5befca90e38aaf5'
    assert is_uuid is True
