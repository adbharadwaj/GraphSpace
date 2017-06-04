from graphspace_python.api.config import GRAPHS_PATH
from graphspace_python.api.obj.single_graph_response import SingleGraphResponse
from graphspace_python.api.obj.multiple_graph_response import MultipleGraphResponse

class Graphs(object):

	def __init__(self, client):
		self.client = client

	def post_graph(self, graph, is_public=0):
		"""Posts NetworkX graph to the requesting users account on GraphSpace.

		:param graph: GSGraph object.
		:param is_public: 1 if graph is public else 0
		:return: Graph Object
		"""

		return SingleGraphResponse(
			self.client._make_request("POST", GRAPHS_PATH,
			                          data={
				                          'name': graph.get_name(),
				                          'is_public': 0 if is_public is None else is_public,
				                          'owner_email': self.client.username,
				                          'graph_json': graph.compute_graph_json(),
				                          'style_json': graph.get_style_json()
			                          }).json()
		)

	def get_graph(self, name, owner_email=None):
		"""Get a graph owned by requesting user with the given name.

		:return: Dict with graph details if a graph with given name exists otherwise None.
		"""
		response = self.client._make_request("GET", GRAPHS_PATH, url_params={
			'owner_email': self.client.username if owner_email is None else owner_email,
			'names[]': name
		}).json()

		if response.get('total', 0) > 0:
			return SingleGraphResponse(
				response.get('graphs')[0]
			)
		else:
			return None

	def get_graph_by_id(self, graph_id):
		"""Get a graph by id.

		:return: Dict with graph details if a graph with given id exists otherwise None.
		"""
		graph_by_id_path = GRAPHS_PATH + str(graph_id)
		return SingleGraphResponse(
			self.client._make_request("GET", graph_by_id_path).json()
		)

	def get_public_graphs(self, tags=None, limit=20, offset=0):
		"""Get public graphs.

		:param tags: Search for graphs with the given given list of tag names. In order to search for graphs with given tag as a substring, wrap the name of the tag with percentage symbol. For example, %xyz% will search for all graphs with 'xyz' in their tag names.
		:param offset: Offset the list of returned entities by this number. Default value is 0.
		:param limit: Number of entities to return. Default value is 20.
		:return: List of Graphs
		"""
		query = {
			'is_public': 1,
			'limit': limit,
			'offset': offset
		}

		if tags is not None:
			query.update({'tags[]': tags})

		return MultipleGraphResponse(
			self.client._make_request("GET", GRAPHS_PATH, url_params=query).json()
		)

	def get_shared_graphs(self, tags=None, limit=20, offset=0):
		"""Get graphs shared with the groups where requesting user is a member.

		:param tags: Search for graphs with the given given list of tag names. In order to search for graphs with given tag as a substring, wrap the name of the tag with percentage symbol. For example, %xyz% will search for all graphs with 'xyz' in their tag names.
		:param offset: Offset the list of returned entities by this number. Default value is 0.
		:param limit: Number of entities to return. Default value is 20.
		:return: List of Graphs
		"""
		query = {
			'member_email': self.client.username,
			'limit': limit,
			'offset': offset
		}

		if tags is not None:
			query.update({'tags[]': tags})

		return MultipleGraphResponse(
			self.client._make_request("GET", GRAPHS_PATH, url_params=query).json()
		)

	def get_my_graphs(self, tags=None, limit=20, offset=0):
		"""Get graphs created by the requesting user.

		:param tags: Search for graphs with the given given list of tag names. In order to search for graphs with given tag as a substring, wrap the name of the tag with percentage symbol. For example, %xyz% will search for all graphs with 'xyz' in their tag names.
		:param offset: Offset the list of returned entities by this number. Default value is 0.
		:param limit: Number of entities to return. Default value is 20.
		:return: List of Graphs
		"""
		query = {
			'owner_email': self.client.username,
			'limit': limit,
			'offset': offset
		}

		if tags is not None:
			query.update({'tags[]': tags})

		return MultipleGraphResponse(
			self.client._make_request("GET", GRAPHS_PATH, url_params=query).json()
		)

	def delete_graph(self, name):
		"""Delete graph with the given name.

		:param name: Name of the graph

		:return: Success/Error Message from GraphSpace
		"""
		response = self.get_graph(name)
		if response is None or response.graph.id is None:
			raise Exception('Graph with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
		else:
			graph_by_id_path = GRAPHS_PATH + str(response.graph.id)
			return self.client._make_request("DELETE", graph_by_id_path).json()

	def update_graph(self, name, owner_email=None, graph=None, is_public=None):
		"""Update graph with the given name with given details.

		:param name: Name of the graph
		:param owner_email: Email of owner of the graph.
		:param graph: GSGraph object.
		:param is_public: 1 if graph is public else 0

		:return: Graph
		"""
		if graph is not None:
			data = {
				'name': graph.get_name(),
				'is_public': 0 if is_public is None else is_public,
				'graph_json': graph.compute_graph_json(),
				'style_json': graph.get_style_json()
			}
		else:
			data = {
				'is_public': 0 if is_public is None else is_public,
			}

		response = self.get_graph(name, owner_email=owner_email)
		if response is None or response.graph.id is None:
			raise Exception('Graph with name `%s` doesnt exist for user `%s`!' % (name, self.client.username))
		else:
			graph_by_id_path = GRAPHS_PATH + str(response.graph.id)
			return SingleGraphResponse(
				self.client._make_request("PUT", graph_by_id_path, data=data).json()
			)

	def make_graph_public(self, name):
		"""Makes a graph publicly viewable.

		:param name: Name of the graph.
		:return: Graph
		"""

		return self.update_graph(name, is_public=1)

	def make_graph_private(self, name):
		"""Makes a graph privately viewable.

		:param name: Name of the graph.
		:return: Graph
		"""
		return self.update_graph(name, is_public=0)
