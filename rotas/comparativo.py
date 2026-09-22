from flask import jsonify
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from schemas.calculo import (
    CalculoEnergiaQuerySchema,
    CalculoEnergiaViewSchema,
    ErrorSchema,
    apresenta_calculo_energia
)
from services.energia_service import calcular_custo_energia

comparativo_tag = Tag(name="Comparativo", description="Rotas de comparativo de custos energéticos")
bp_comparativo = APIBlueprint('comparativo', __name__, abp_tags=[comparativo_tag])

@bp_comparativo.get('/comparar-custo', summary="Calcula o custo mensal de energia de um veículo elétrico", responses={
        200: CalculoEnergiaViewSchema,
        400: ErrorSchema,
        500: ErrorSchema
    }
)
def comparar_custo_rota(query: CalculoEnergiaQuerySchema):
    """
    Calcula o custo estimado de energia elétrica com base na quilometragem, 
    consumo por km e na tarifa oficial de energia obtida via API da ANEEL para a UF informada.
    """
    try:
        # Chama o serviço que realiza a busca na ANEEL e efetua os cálculos
        resultado = calcular_custo_energia(
            km_mensal=query.km_mensal,
            consumo_kwh_por_km=query.consumo_kwh_por_km,
            uf=query.uf
        )

        return jsonify(apresenta_calculo_energia(resultado)), 200

    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": "Erro interno ao processar o comparativo.", "error": str(e)}), 500