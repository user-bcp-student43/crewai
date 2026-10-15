"""Agente frontend que implementa funcionalidades Angular."""

from crewai import Agent, Task
from crew.llm_config import llm

KEY = "frontend"
LABEL = "Desarrollador frontend"
SPEC_FILE = "frontend_spec.md"
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa la funcionalidad frontend descrita, priorizando el contrato API y los criterios de aceptación.

Antes de proponer código, identifica la pantalla, acciones, datos, validaciones y estados necesarios. Usa Angular 17 y TypeScript salvo que el contexto aprobado indique otra versión o patrón; respeta la estructura, convenciones, componentes y dependencias existentes. Si falta un dato del contrato, no inventes endpoints, campos ni reglas: deja explícita la suposición mínima o señala qué información hace falta.

Entrega los archivos que la funcionalidad realmente necesite, usando tipos explícitos y responsabilidades claras:
- Componentes para presentación e interacción; servicios para llamadas HTTP y lógica reutilizable; modelos para contratos de datos.
- Integra rutas, guards o interceptores solo cuando los requiera la funcionalidad y el contexto existente.
- Representa los estados de carga, vacío, éxito y error que correspondan, con mensajes útiles y sin ocultar fallos del backend.
- Usa Reactive Forms cuando haya formularios, con validación coherente, etiquetas asociadas y mensajes de error accesibles.
- Construye una interfaz responsive y accesible: HTML semántico, navegación por teclado, foco visible, etiquetas y estados accesibles; no dependas solo del color.
- Muestra contenido dinámico como texto interpolado; no uses innerHTML ni desactives la sanitización.
- No guardes tokens en localStorage, no expongas credenciales o detalles técnicos en la UI, y no agregues dependencias sin autorización.
- No dupliques lógica de HTTP o sesión ni cambies contratos existentes.

Devuelve cada archivo en un bloque Markdown separado y nómbralo en la primera línea del bloque con un comentario válido, por ejemplo `// login.component.ts` o `<!-- login.component.html -->`. Usa nombres de archivo con extensión .ts, .html o .css; el extractor del flujo no conserva directorios. Incluye solo código necesario para la funcionalidad. Si recomiendas pruebas o comandos, identifícalos como pendientes: no afirmes que ejecutaste pruebas, lint o build."""

agent = Agent(
    role=LABEL,
    goal="Implementar funcionalidades Angular accesibles, seguras y alineadas con los requisitos y el contrato API.",
    backstory="Eres especialista en frontend Angular y TypeScript. Conviertes historias de usuario en interfaces mantenibles, accesibles y responsive, integradas con APIs sin inventar contratos ni ocultar errores.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


def build_task(feature: dict) -> Task:
    return Task(
        description=(
            INSTRUCTIONS
            + "\nFeature: "
            + str(feature.get("title", ""))
            + "\n"
            + str(feature.get("description", ""))
            + "\n"
            + str(feature.get("acceptance_criteria", []))
        ),
        expected_output=(
            "Bloques Markdown de código, uno por archivo; primera línea con el "
            "nombre de archivo en un comentario, por ejemplo // nombre.service.ts. "
            "Incluye únicamente archivos .ts, .html o .css necesarios."
        ),
        agent=agent,
    )
