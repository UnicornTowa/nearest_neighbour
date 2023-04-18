# Алгоритмы
import networkx as nx

# Алгоритм ближайшего соседа
def nna(graph:nx.Graph, start_v):
    # Определяем объекты, которые будем возвращать
    out_graph = nx.DiGraph()
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
            return out_graph, 0

        # Выбираем ребро наименьшей длины
        chosen_edge = min(edges, key=lambda x: x[2]['weight'])

        # Новая вершина цикла и длина пути до неё
        new_v = chosen_edge[1]
        weight = chosen_edge[2]['weight']

        # Добавляем элементы в выходной граф и объекты вывода, обновляем счетчик
        out_graph.add_edge(current_v, new_v, weight=weight)
        path_len += weight
        visited_count += 1

        # Помечаем вершину как посещенную, удаляем ребро из исходного графа
        graph.nodes[new_v]['visited'] = True
        current_v = new_v

    # Если вершин больше 2-х - добавляем ребро, замыкающее цикл
    if vertex_count != 1:
        if graph.has_edge(current_v, start_v) and vertex_count != 2:
            final_edge = graph.edges[current_v, start_v]
            path_len += final_edge['weight']
            out_graph.add_edge(current_v, start_v, weight=final_edge['weight'])
        else:
            return out_graph, 0
    return out_graph, path_len

# Оптимизация простых петель
def two_opt(graph: nx.Graph, res_graph: nx.DiGraph):
    # Перебираем все ребра выходного графа
    for edge in res_graph.edges(data=True):
        b_c = edge
        # Определяем точки A, B, C, D если ребра существуют
        a_edges = list(res_graph.in_edges(b_c[0], data=True))
        d_edges = list(res_graph.out_edges(b_c[1], data=True))
        if a_edges and d_edges:
            a_b = a_edges[0]
            c_d = d_edges[0]
            a = a_b[0]
            b = a_b[1]
            c = c_d[0]
            d = c_d[1]
        else:
            continue
        if not graph.has_edge(a, c) or not graph.has_edge(b, d):
            continue
        a_c_len = graph.edges[a, c]['weight']
        b_d_len = graph.edges[b, d]['weight']
        old_weight = a_b[2]['weight'] + c_d[2]['weight']
        new_weight = a_c_len + b_d_len
        # Проверяем есть ли улучшение, если есть - изменяем решение
        if new_weight < old_weight:
            res_graph.remove_edges_from([a_b, c_d])
            res_graph.add_edge(a, c, weight=a_c_len)
            res_graph.add_edge(b_c[1], b_c[0], weight=b_c[2]['weight'])
            res_graph.add_edge(b, d, weight=b_d_len)

            res_graph.remove_edges_from([b_c])

            improve = old_weight - new_weight
            # Возвращаем насколько улучшили путь
            return improve
    # Если не нашли, возвращаем 0
    return 0

# Разворот двойных петель
def vertex_opt(graph: nx.Graph, res_graph: nx.DiGraph):
    # Перебираем вершины выходного графа
    for vertex in res_graph.nodes:
        # Определяем вершины A, B, C, D, E, если их возможно определить
        c = vertex
        b_edges = list(res_graph.in_edges(c, data=True))
        d_edges = list(res_graph.out_edges(c, data=True))
        if b_edges and d_edges:
            b_c = b_edges[0]
            c_d = d_edges[0]
            b = b_c[0]
            d = c_d[1]
        else:
            continue
        a_edges = list(res_graph.in_edges(b, data=True))
        e_edges = list(res_graph.out_edges(d, data=True))
        if a_edges and e_edges:
            a_b = a_edges[0]
            d_e = e_edges[0]
            a = a_b[0]
            e = d_e[1]
        else:
            continue
        if not graph.has_edge(a, d) or not graph.has_edge(b, e):
            continue
        a_d_len = graph.edges[a, d]['weight']
        b_e_len = graph.edges[b, e]['weight']
        old_weight = a_b[2]['weight'] + d_e[2]['weight']
        new_weight = a_d_len + b_e_len
        # Проверяем есть ли улучшения, если есть - изменяем решение
        if new_weight < old_weight:
            res_graph.remove_edges_from([a_b, d_e])
            res_graph.add_edge(a, d, weight=a_d_len)
            res_graph.add_edge(c_d[1], c_d[0], weight=c_d[2]['weight'])
            res_graph.add_edge(b_c[1], b_c[0], weight=b_c[2]['weight'])
            res_graph.add_edge(b, e, weight=b_e_len)

            res_graph.remove_edges_from([b_c, c_d])
            # Возвращаем насколько улучшили решение
            improve = old_weight - new_weight
            return improve
    # Не улучшили - возвращаем 0
    return 0
