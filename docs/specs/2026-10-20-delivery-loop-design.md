# delivery-loop — diseño

Fecha: 2026-10-20 · Estado: borrador para revisión

## 1. Objetivo

Un plugin de Claude Code que hace seguir un ciclo de entrega completo —de la fuente de la
tarea (ticket, documento del cliente, petición) hasta el cambio verificado en vivo, promovido
y cerrado— en cualquier entorno de trabajo, sin depender de herramientas concretas.

- El **núcleo es público y agnóstico**: no nombra ninguna empresa, tracker, host de git ni
  plataforma de deploy. Habla de capacidades abstractas y de comportamientos.
- Lo concreto de cada entorno vive en **perfiles por niveles** (usuario, organización,
  proyecto, repo) que se rellenan en el primer uso con un **censo** y se reutilizan después.
- El primer caso concreto es un perfil de organización real, que vive en un repo privado aparte;
  este repo solo contiene perfiles de ejemplo ficticios.
- Meta secundaria: **pocas confirmaciones**. Lo que se puede decidir de antemano se decide una
  vez (perfil o pre-decisiones de la tarea) y no se vuelve a preguntar.

Fuera de alcance: sustituir a los revisores humanos o a las protecciones de rama; ejecutar
builds o suites que el perfil prohíba en local; gestionar la infraestructura del entorno.

## 2. Principios de diseño

1. **Declarar comportamiento, no procedimiento.** Cada fase fija qué entra, qué sale y la prueba
   de que está hecha. El cómo lo elige Claude con las capacidades disponibles.
2. **Detectar antes de preguntar.** Lo que se puede deducir del repo, del host o de la sesión
   no se pregunta.
3. **Preguntar una vez.** Toda respuesta queda escrita en el perfil (si es duradera) o en las
   pre-decisiones de la tarea (si no lo es).
4. **Evidencia antes que afirmación.** Ninguna fase se cierra con «lo he revisado»; se cierra con
   una salida de comando, un test, una captura o una consulta. «Leído en código» y «medido en el
   entorno» se distinguen siempre.
5. **Autocontenido.** No exige otros plugins. Si la sesión tiene skills equivalentes (p. ej.
   brainstorming, TDD, depuración sistemática), puede delegar en ellas; sin ellas, el contrato de
   la fase basta.

## 3. Estructura del plugin

```
delivery-loop/
  .claude-plugin/plugin.json
  skills/
    deliver/            orquestador: contratos de fase y comportamientos transversales
      phases/*.md       un fichero por fase, cargado al entrar en ella
    census/             primer uso y re-comprobación: detecta, pregunta lo que falta, escribe perfiles
    spec/               inventario de la fuente con IDs estables, huecos, documento de revisión
    qa-design/          plan de verificación por ID a partir del inventario
    qa-execution/       ejecución del plan contra el entorno desplegado, evidencias, bugs fuera de spec
  profile/
    schema.md           capacidades y campos posibles de un perfil
    defaults.md         política por defecto (ver §7)
  examples/             un perfil de ejemplo por nivel
  docs/specs/           este documento
```

`spec`, `qa-design` y `qa-execution` salen de las skills homónimas existentes, generalizadas:
se retira toda referencia a herramientas o clientes concretos.

## 4. Capacidades

El núcleo solo conoce estas capacidades. Cada perfil dice con qué se implementa cada una en
su entorno, o que no existe.

| Capacidad | Qué resuelve | Ejemplos |
|---|---|---|
| `tracker` | De dónde sale la spec y dónde se refleja el estado | Linear, Jira, GitHub Issues, documento del cliente, ninguno |
| `vcs` | Host, ramas, protección, cómo se crea el espacio aislado | GitHub, GitLab, Azure DevOps |
| `ci` | Qué corre en cada evento (borrador, listo, merge) y qué checks son obligatorios | GitHub Actions, otro, ninguno |
| `environments` | Qué entornos hay, cuál es producción, qué rama va a cada uno, URLs | dev/staging/prod |
| `deploy` | Cómo llega un cambio a cada entorno y cómo se comprueba qué SHA se sirve | integración con Git, pipeline, manual |
| `reviewers` | Quién revisa el diff y con qué peso | humano, bot que aprueba, revisor adversarial con otro modelo, subagente |
| `live-verification` | Con qué se verifica en un entorno desplegado | navegador automatizado, peticiones HTTP, consultas a la BD de pruebas |
| `channels` | Por dónde se avisa o se piden aprobaciones | chat del equipo, correo, ninguno |
| `machine` | Límites de la máquina local | concurrencia de tests, qué no se ejecuta en local, SO |
| `authority` | Ajustes al modelo de autoridad (§7) | «el merge a producción lo hace un bot si aprueba» |

## 5. Perfiles por niveles

### 5.1 Ubicación

Un fichero `.delivery/profile.md` en cada nivel que lo necesite. Al arrancar, el script
`scripts/merge_profiles.py` recoge, de lejos a cerca:

0. `profile/defaults.md` del propio plugin (nivel 0, siempre presente);
1. el de usuario, `~/.claude/delivery/profile.md`;
2. cada `.delivery/profile.md` desde la raíz del sistema de ficheros hasta el directorio de
   trabajo.

Reglas del recorrido: rutas resueltas y deduplicadas sin distinguir mayúsculas en Windows;
`~/.delivery/profile.md` no es válido (error que remite al de usuario); por encima del repo
actual se ignoran los directorios que sean a su vez raíz de un repo git, para que un worktree
anidado no recoja el perfil del checkout principal.

| Nivel | Ubicación típica | Contenido típico | Se comparte |
|---|---|---|---|
| Usuario | `~/.claude/delivery/profile.md` | `machine`, herramientas conectadas en la sesión | no |
| Organización | directorio que agrupa los repos de la organización | `tracker`, convenciones de `vcs` y `ci`, `reviewers`, `channels` | se distribuye desde un repo de la organización |
| Proyecto | directorio que agrupa los repos de un cliente o producto | excepciones del proyecto (entorno del cliente, revisores no disponibles) | según el equipo |
| Repo | `<repo>/.delivery/profile.md`, commiteado | `environments`, `deploy`, `ci` concretos del repo | sí, con el repo |

### 5.2 Combinación

- Cada nivel aplica a todo lo que queda por debajo.
- **Campos**: gana el nivel más cercano al repo.
- **Reglas**: se acumulan de todos los niveles; cada regla tiene un id (por sección) y un nivel
  inferior con el mismo id la sustituye.
- **Invariantes**: una regla `[invariant id]` o un campo `- clave: valor [invariant]` no lo
  puede cambiar un nivel inferior: se conserva y se informa del conflicto. El id de una
  invariante queda reservado en todas las secciones. Repetir una
  invariante con el mismo texto no es conflicto.
- Las contradicciones semánticas con otro id no las detecta el script: las revisa Claude en la
  fase 0 al leer el perfil combinado.
- El perfil combinado anota el nivel de origen de cada campo y regla.

### 5.3 Formato

Markdown, una sección por capacidad, con palabras clave en inglés aunque el contenido esté en
otro idioma (el script las analiza). Gramática completa en `profile/schema.md`.

```markdown
## deploy
- via: git-integration
- production-env: prod [invariant]
Rules:
- [invariant no-prod-testing] Never test or write against production.
- [no-cli-deploy] Deploy only through the git integration, never from a CLI.
- [served-sha] A successful deploy is not serving: check the served SHA.
Source: deploy config + platform API · checked 2026-10-20
```

## 6. Censo

Skill `census`. Corre en la fase 0.

### 6.1 Primer uso en un repo

1. **Detectar sin preguntar**: remoto y host de git; protección de ramas (por API); ficheros de
   CI y qué corre en cada evento; configuración de deploy; MCPs y skills de la sesión; CLIs
   instaladas; frameworks de test.
2. **Asignar capacidades**: cada hallazgo va a su capacidad, y cada capacidad toma la mejor
   implementación disponible (p. ej. revisor adversarial con otro modelo si está conectado; si
   no, la revisión integrada más un subagente).
3. **Preguntar solo lo no deducible**, en una sola ronda, una pregunta por dato, con la opción
   recomendada primero.
4. **Proponer el nivel de cada dato** según su naturaleza (§5.1). Un dato que ya está en un nivel
   superior no se duplica.
5. **Escribir** los perfiles, enseñando antes el contenido nuevo o cambiado.
6. **Proponer la lista de permisos** del harness (§7.4).

### 6.2 Usos siguientes

Comprobación barata en la fase 0: los datos clave del perfil (remoto, protección de ramas,
configuración de deploy) siguen cuadrando con lo detectado. Si algo cambió, se actualiza ese
dato y se dice. Un dato cuya procedencia tiene mucha antigüedad se re-verifica antes de
apoyarse en él.

## 7. Autoridad

### 7.1 Clases de acción (`profile/defaults.md`)

| Clase | Ejemplos | Por defecto |
|---|---|---|
| Local y reversible | leer, espacio aislado, commits, tests de la zona | sin preguntar |
| Propio y respaldable | push de su rama, PR en borrador, revisores, mover o comentar el ticket | sin preguntar |
| Entorno de pruebas | merge a la rama de integración, deploy por la vía declarada, variables del entorno de pruebas, e2e en vivo | sin preguntar, salvo que el perfil diga otra cosa |
| Producción y ramas protegidas | merge a la rama de producción, variables de producción | preguntar, o seguir la vía declarada en el perfil (bot que aprueba, canal de aprobaciones) |
| Hacia terceros | mensajes, correos, comentarios que ve el cliente | enseñar el texto y pedir visto bueno |
| Irreversible | force-push, borrar ramas sin mergear, borrar datos | preguntar, con dos excepciones para borrar datos: el borrado está pedido expresamente en el plan, o son datos de prueba creados por Claude durante la tarea que no hace falta conservar |

Cada perfil puede mover acciones entre clases, salvo contra una invariante.

### 7.2 Pre-decisiones

En la fase 0, una ronda única con lo que el perfil no resuelve para esta tarea: datos reales que
se pueden leer o escribir; verificaciones que solo puede hacer un humano; acciones de la tarea
fuera de su clase. Se escriben como `D0.x` en el **fichero de tarea**
(`.delivery/tasks/<slug>.md`, creado en la fase 0, ignorado por git salvo que el perfil diga lo
contrario), junto con el tamaño y los escalados; el plan de la fase 3 lo incorpora. Lo no
contestado se convierte en una condición de escalado con nombre, nunca en una suposición.

### 7.3 Escalado durante la tarea

Una pregunta por decisión, con 2–4 opciones y la recomendada primero. Mientras espera,
Claude avanza en todo lo que no dependa de la respuesta. La respuesta va al perfil si es
duradera y al fichero de tarea si no lo es.

### 7.4 Permisos del harness y guardas

- El censo propone una lista de permisos permitidos (`.claude/settings.json`) con los comandos
  detectados de las tres primeras clases. Se enseña antes de escribirse y se fusiona a mano con
  la existente; nunca se sobrescribe.
- Opcional: las invariantes expresables como patrón de comando se generan como hook que las
  bloquea.

## 8. Fases

Cada fase vive en `skills/deliver/phases/<n>-<nombre>.md` con su contrato.

| # | Fase | Entra | Sale | Hecha cuando |
|---|---|---|---|---|
| 0 | Arranque | tarea + perfil combinado | censo vigente; tamaño de la tarea con motivo; pre-decisiones `D0.x`; espacio aislado sobre la base actualizada | toda capacidad que pide la tarea está resuelta o marcada «escalar» |
| 1 | Spec | la fuente completa (ticket con comentarios y adjuntos, documento, petición) | inventario con IDs estables; precedencia fuente > spec > plan > código | cada punto de la fuente tiene ID o está excluido con motivo |
| 2 | Huecos | inventario | decisiones que solo puede tomar un humano, cada una con recomendación | ningún hueco abierto bloquea el plan |
| 3 | Plan | inventario + código real leído | pasos pequeños, cada uno con los IDs que cubre y su test; alcance cerrado | revisado por un agente; todo ID tiene paso |
| 4 | Implementación | plan | commits test que falla → código → test que pasa | tests de la zona tocada en verde, ejecutados |
| 5 | Revisión | diff completo + spec | veredicto de los revisores disponibles; cada hallazgo arreglado, rebatido con prueba o aplazado con ticket | nada bloqueante abierto |
| 6 | Integración | rama revisada | PR (en borrador si el entorno lo usa), merge a la rama de integración, deploy al entorno de pruebas | el entorno sirve el SHA exacto, comprobado |
| 7 | Verificación en vivo | plan de QA del inventario | estado y evidencia de cada ID; bugs fuera de spec aparte; smoke de no regresión | todo ID en PASS o escalado explícito; evidencia visual siempre que exista algo que ver |
| 8 | Promoción | PR lista | PR a la rama de producción, CI completa del último commit, aprobación válida | merge comprobado contra git |
| 9 | Cierre | merge | ticket actualizado; evidencias enlazadas en PR y ticket; ramas y espacios aislados limpios; informe | estado del tracker y de git coincide con el informe |

### 8.1 Evidencia y no regresión (fases 7 y 9)

- **Evidencia visual obligatoria en el cierre**: capturas o grabación de cada ID verificado en el
  entorno desplegado, enlazadas en la PR y en el ticket. Un ID sin superficie visual (API, cola)
  aporta la respuesta real o la consulta, con fecha y entorno. Un ID sin evidencia no se cierra.
- **Prueba de que no se ha roto nada más**: CI completa del último commit en verde; smoke en vivo
  de los flujos vecinos que comparten código con el cambio (deducidos del diff: quién importa lo
  tocado); comparación antes/después en el mismo entorno cuando hay baseline.
- El informe de cierre separa «lo pedido funciona» de «lo demás sigue funcionando».

### 8.2 Escala

Claude decide el tamaño en la fase 0 y lo escribe con su motivo.

| Tamaño | Fases |
|---|---|
| Trivial | 0 (con mini-inventario de IDs sacado de la petición) → 4 → 5 → 6 → 7 (esos IDs + smoke) → 8 → 9 |
| Feature | todas |
| Rediseño grande | todas; en 1, inventario de partida con lectores en paralelo y crítico de completitud; en 3, un plan por PR con checkpoint humano entre PRs |

### 8.3 Comportamientos transversales

- Verificar en la fuente (código, entorno, documento original), no en un resumen o memoria.
- Las decisiones obvias se toman y se escriben: «Decidido: …, porque …».
- Un test viejo que codifica el defecto se enmienda explicando por qué; el arreglo no se recorta.
- Nada más ni menos que el alcance acordado.
- Un bloqueo o un hueco se comprueba antes de declararlo.
- El informe al usuario: qué se decidió y por qué, qué queda abierto con recomendación, qué se
  asumió, qué quedó fuera y dónde mirar.

## 9. Perfiles de organización reales

Un perfil de organización real vive en un repo privado de esa organización, nunca en este. Este
repo solo trae `examples/` con una organización ficticia. El repo privado aporta además su lista
de términos propios para la comprobación de agnosticismo (§10) y la ejecuta en su propio CI.
Los datos personales (cuentas, máquina) van al perfil de usuario de cada persona, no al de
organización.

## 10. Verificación del propio plugin

- **Evals de disparo y de comportamiento** por skill: casos con y sin perfil, con capacidades
  ausentes, con una invariante en conflicto. Se escriben tras el primer ensayo real, a partir de
  sus fallos.
- **Prueba de agnosticismo**: falla si el núcleo (`skills/`, `profile/`, `scripts/`, `README.md`)
  menciona una herramienta concreta fuera de las líneas marcadas como ejemplo. La lista pública
  solo tiene nombres de herramientas; los nombres de empresas y clientes llegan de un fichero
  externo (`--denylist`) que aporta cada repo privado.
- **Prueba de combinación de perfiles**: fixtures de cuatro niveles más los valores por defecto,
  con conflicto de campo, regla sustituida, regla acumulada e invariante relajada; el perfil
  combinado esperado se compara byte a byte con un fichero dorado.
- **Ensayo real**: una tarea de un tracker real recorrida de punta a punta con un perfil de
  organización privado, y un repo personal sin tracker con solo el perfil de usuario.

## 11. Decisiones

- **Idioma**: núcleo en inglés (alcance público); los perfiles, en el idioma de cada equipo, con
  las palabras clave de la gramática en inglés.
- **Estilo de las skills y perfiles**: registro técnico compacto para ahorrar tokens: `clave:
  valor`, tablas, imperativos breves, símbolos (`→`, `≠`). Sin prosa explicativa, sin
  ejemplos redundantes. La razón de una regla, solo si cambia cómo se aplica (≤ 1 línea).
  Este spec es la excepción: está en prosa para la discusión de diseño.
- **Revisión de spec y plan**: la hace un agente auditor, no el usuario. Ningún gate del
  plugin depende de que una persona lea un documento; las decisiones se cierran en la
  conversación.
