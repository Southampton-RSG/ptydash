from ptydash.cards.image_card import ImageCard

def test_client():
    card = ImageCard(None, hostname="wonderbox.ecs.soton.ac.uk", topic_id="test_topic")
    assert len(card.client_list) >= 0, 'client does not exist'
    for clientname1 in range(len(card.client_list)):
        for clientname2 in range(clientname1 + 1, len(card.client_list)):
            assert card.client_list[clientname1] != card.client_list[clientname2], 'client ID not unique'


    assert card.host != None, 'update hostname in config file'
    assert card.topic_name != None, 'invalid topic ID, update topic_id in config file'

def test_graphprocedure():
    card = ImageCard(None, hostname="wonderbox.ecs.soton.ac.uk", topic_id="test_topic")
    spoofdata = "testheader: 27 testheader2: 99"
    card.get_graph(spoofdata)
    assert len(card.x_data_storage) > 0, 'MQTT data not received'
    assert len(card.y_data_storage) > 0, 'MQTT data not received'
    assert len(card.data_list) != 0, 'No data'
    print(card.data_list)

    for data in card.x_data_storage:
        assert type(data) == int or type(data) == float, 'invalid data format, int or float expected'
    for data in card.y_data_storage:
        assert type(data) == int or type(data) == float, 'invalid data format, int or float expected'
    assert type(card.data_list[0]) == str, 'invalid data format, string expected'
    assert type(card.data_list[2]) == str, 'invalid data format, string expected'





