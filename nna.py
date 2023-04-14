import networkx as nx

def nna(graph:nx.Graph, start_v):
    # Определяем объекты, которые будем возвращать
    out_graph = nx.Graph()
    path = str(start_v)
    path_len = 0

    # Подготовка
    vertex_count = len(graph.nodes)
    visited_count = 1
    out_graph.add_node(start_v)
    current_v = start_v

    # Помечаем вершины кроме текущей
    nx.set_node_attributes(graph, {n: {'visited': True if n == start_v else False} for n in graph.nodes()})

    # Основной цикл
    while visited_count != vertex_count:
        # Получаем все ребра, соединяющие текущую вершину с непосещенными
        edges = [edge for edge in graph.edges(current_v, data=True) if graph.nodes[edge[1]]['visited'] == False]

        # Возврат если таких вершин нет
        if len(edges) == 0:
            return out_graph, 'No solution found', path_len

        # Выбираем ребро наименьшей длины
        chosen_edge = min(edges, key=lambda x: x[2]['weight'])

        # Новая вершина цикла и длина пути до неё
        new_v = chosen_edge[1]
        weight = chosen_edge[2]['weight']

        # Добавляем элементы в выходной граф и объекты вывода, обновляем счетчик
        out_graph.add_edge(current_v, new_v, weight=weight)
        path += ' -> ' + str(new_v)
        path_len += weight
        visited_count += 1

        # Помечаем вершину как посещенную, удаляем ребро из исходного графа
        graph.nodes[new_v]['visited'] = True
        graph.remove_edge(current_v, new_v)
        current_v = new_v

    # Если вершин больше 1-й - добавляем ребро, замыкающее цикл
    if vertex_count != 1:
        if graph.has_edge(current_v, start_v):
            final_edge = graph.edges[current_v, start_v]
            path += ' -> ' + str(start_v)
            path_len += final_edge['weight']
            out_graph.add_edge(current_v, start_v, weight=final_edge['weight'])
        else:
            return out_graph, 'No solution found', None
    return out_graph, path, path_len
