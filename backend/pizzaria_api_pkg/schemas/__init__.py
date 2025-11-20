from .usuarios import Usuario, UsuarioCreate
from .clientes import Cliente, ClienteCreate
from .produtos import Produto, ProdutoCreate
from .categorias_produto import CategoriaProduto, CategoriaProdutoCreate
from .ingredientes import Ingrediente, IngredienteCreate
from .avaliacoes import AvaliacaoOut, AvaliacaoCreate
from .pizza_personalizada import PizzaOut, PizzaCreate
from .pizza_ingrediente import PizzaIngrediente, PizzaIngredienteCreate
from .cupons import CupomCreate, CupomResponse

model_config = {
    "from_attributes": True
}
