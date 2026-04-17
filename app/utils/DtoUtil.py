from typing import TypeVar

T = TypeVar("T")


def patch(obj: T, dto) -> T:
    """
    Atualiza parcialmente os atributos de um objeto a partir de um dto de entrada.

    Este método aplica um comportamento equivalente a um PATCH: apenas os campos
    explicitamente definidos no dto são utilizados para atualizar o objeto,
    preservando os demais valores já existentes.

    A função converte o dto para dicionário utilizando `exclude_unset=True`,
    garantindo que apenas os campos enviados sejam considerados. Em seguida,
    cada atributo é atualizado dinamicamente via `setattr`.

    Parâmetros:
        obj (T): Instância do modelo a ser atualizada.
        dto: Objeto de dto (ex: Pydantic) contendo os dados de atualização.

    Retorno:
        T: A mesma instância do objeto, com os atributos atualizados.

    Observações:
        - Não realiza validação adicional além da já feita pelo dto.
        - Pode sobrescrever atributos com `None` caso estes sejam explicitamente enviados.
    """
    update_data = dto.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if hasattr(obj, field):
            setattr(obj, field, value)

    return obj
