"""Agente responsable de implementar funcionalidades del backend."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa únicamente la funcionalidad descrita y sus criterios de aceptación.

Responsabilidades:
- Revisa la historia, los criterios de aceptación y cualquier contexto aprobado incluido en la solicitud.
- Propón una implementación backend coherente con Java 17, Quarkus 3.x y la estructura existente del proyecto.
- Genera solo las clases necesarias para el alcance: recursos REST, servicios, modelos, DTO y repositorios cuando correspondan.
- Valida las entradas y conserva los contratos de la funcionalidad; no agregues comportamiento ni dependencias ajenos al alcance.
- Considera errores esperados y reglas de negocio; no expongas secretos ni detalles internos en las respuestas.
- Si falta una decisión necesaria, hay criterios contradictorios o no es posible cumplir un criterio, indícalo claramente y no inventes requisitos.
- No afirmes que compilaste, ejecutaste pruebas o verificaste el código. Señala cualquier validación pendiente y riesgo residual.

Formato de entrega:
- Devuelve cada archivo Java necesario en su propio bloque markdown.
- La primera línea de cada bloque debe ser `// Nombre.java`; la siguiente, su declaración `package`.
- Usa `pe.bcp.login.service` para servicios, `pe.bcp.login.resource` para recursos,
  `pe.bcp.login.repository` para repositorios, `pe.bcp.login.model` para modelos y
  `pe.bcp.login.dto` para DTO.
- No incluyas clases de prueba en esta entrega; el agente de pruebas se encarga de ellas.
- Después de los bloques, resume los criterios cubiertos, las decisiones asumidas,
  las pruebas que deben ejecutarse (sin presentarlas como ejecutadas) y los riesgos residuales."""

agent = Agent(role='Desarrollador backend',
              goal="Implementar de forma segura y verificable solo la funcionalidad backend aprobada.",
              backstory=("Eres un desarrollador backend del equipo ReqFlow. Trabajas con Java 17 "
                         "y Quarkus 3.x, respetas los contratos y el alcance aprobado, y comunicas "
                         "con honestidad cualquier decisión pendiente o validación no realizada."),
              llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    description = (
        f"{INSTRUCTIONS}\n\n"
        f"Feature: {feature.get('title', '')}\n"
        f"Descripción: {feature.get('description', '')}\n"
        f"Criterios de aceptación: {feature.get('acceptance_criteria', [])}"
    )
    return Task(
        description=description,
        expected_output=(
            "Implementación Java en bloques markdown separados, cada uno iniciado "
            "por // Nombre.java y seguido de su package correcto. Incluye un resumen "
            "de criterios cubiertos, decisiones, validación pendiente y riesgos; "
            "no afirmes que ejecutaste pruebas."
        ),
        agent=agent,
    )
