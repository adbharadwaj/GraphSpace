import pytest
from graphspace_python.graphs.classes.gslayout import GSLayout
from graphspace_python.api.client import GraphSpace
from graphspace_python.api.obj.layout_response import LayoutResponse
from graphspace_python.api import errors


def test_layouts_endpoint(graph_id):
	layout = test_post_graph_layout(graph_id=graph_id, name='MyTestLayout')
	test_layout_name_already_exists_error(graph_id=graph_id, name='MyTestLayout')
	test_get_my_graph_layouts(graph_id=graph_id)
	test_update_graph_layout(graph_id=graph_id, layout_id=layout.id)
	test_get_shared_graph_layouts(graph_id=graph_id)
	test_delete_graph_layout(graph_id=graph_id, layout_id=layout.id)
	test_user_not_authorised_error(graph_id=graph_id, layout_id=layout.id)


def test_user_not_authorised_error(graph_id, layout_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	with pytest.raises(errors.UserNotAuthorised) as err:
		graphspace.get_graph_layout(graph_id, layout_id)


def test_layout_name_already_exists_error(graph_id, name):
	with pytest.raises(errors.LayoutNameAlreadyExists) as err:
		test_post_graph_layout(graph_id=graph_id, name=name)


def test_get_my_graph_layouts(graph_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_my_graph_layouts(graph_id=graph_id)
	assert type(response) is LayoutResponse
	assert hasattr(response, 'layouts') and len(response.layouts) >= 0


def test_get_shared_graph_layouts(graph_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.get_shared_graph_layouts(graph_id=graph_id)
	assert type(response) is LayoutResponse
	assert hasattr(response, 'layouts') and len(response.layouts) >= 0


def test_post_graph_layout(graph_id, name=None):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	layout1 = GSLayout()
	if name is not None:
		layout1.set_name(name)
	layout1.set_node_position('a',45,55)
	layout1.set_node_position('b',36,98)
	layout1.add_node_style('a', shape='ellipse', color='green', width=90, height=90)
	layout1.add_node_style('b', shape='ellipse', color='yellow', width=40, height=40)
	response = graphspace.post_graph_layout(graph_id=graph_id, layout=layout1)
	assert type(response) is LayoutResponse
	assert hasattr(response, 'layout') and response.layout.is_shared == 0
	return response.layout


def test_update_graph_layout(graph_id, layout_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	layout = graphspace.get_graph_layout(graph_id=graph_id, layout_id=layout_id).layout
	layout.set_name('Updated test layout')
	layout.set_node_position('z',74,37)
	layout.set_is_shared()
	response = graphspace.update_graph_layout(graph_id=graph_id, layout_id=layout_id, layout=layout)
	assert type(response) is LayoutResponse
	assert hasattr(response, 'layout') and response.layout.name == layout.get_name()
	assert 'z' in response.layout.positions_json.keys()
	assert response.layout.is_shared == 1


def test_delete_graph_layout(graph_id, layout_id):
	graphspace = GraphSpace('user1@example.com', 'user1')
	graphspace.set_api_host('localhost:8000')
	response = graphspace.delete_graph_layout(graph_id=graph_id, layout_id=layout_id)
	assert response == "Successfully deleted layout with id=" + str(layout_id)
