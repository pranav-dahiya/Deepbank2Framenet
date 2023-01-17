from torch_geometric.data import Data
from torch_geometric.nn import Node2Vec, global_add_pool
import torch


def embedd(sentence):
    data = eds2data(sentence.deepbank.eds)
    x = node2vec(data)
    return x.mean(dim=0)
    
    
def node2vec(data):
    device = 'cuda'
    model = Node2Vec(data.edge_index, embedding_dim=16, walk_length=10, context_size=4).to(device)
    optimizer = torch.optim.Adam(list(model.parameters()), lr=0.01)
    loader = model.loader()

    for epoch in range(1, 101):
        model.train()
        total_loss = 0
        for pos_rw, neg_rw in loader:
            optimizer.zero_grad()
            loss = model.loss(pos_rw.to(device), neg_rw.to(device))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
    
    return model().cpu().detach()


def eds2data(eds):
    node_map = {node.id: i for i, node in enumerate(eds.nodes)}  
    edges = [[node_map[edge[0]] for edge in eds.edges], [node_map[edge[2]] for edge in eds.edges]]
    return Data(edge_index=torch.tensor(edges, dtype=torch.long))