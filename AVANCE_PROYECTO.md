# Avance del Proyecto PATS - Web Animada

Fecha de registro: 2026-04-28

## Objetivo

Construir una experiencia web institucional para el Programa de Apoyo al Transporte Subnacional (PATS), de Provias Descentralizado / MTC, usando una animacion de video sincronizada con el scroll al estilo de paginas de producto.

La web busca comunicar:

- El problema de conectividad vial rural.
- La magnitud de la brecha en caminos vecinales.
- Los componentes principales del PATS.
- El impacto de proyectos, mantenimientos y planes viales.
- Una narrativa visual apoyada por video frame por frame.

## Fuentes y archivos base

- `prompts_animation_VIDEO.TXT`: guia tecnica para construir la animacion con canvas, frames y scroll.
- `video_prueba1.mp4`: video inicial usado para extraer frames.
- `video_prueba1_enhanced.mp4`: version procesada del video con mejora ligera de nitidez, contraste y saturacion.
- `frames/`: secuencia de 192 imagenes JPG usadas por el canvas.
- `REDISEÑO PPT PATS (4).pdf`: presentacion de referencia para contenido, enfoque visual y cifras del PATS.
- `imagen_4k.txt`: prompt auxiliar para mejora/upscale de imagenes.

## Implementacion actual

Archivo principal:

- `index.html`

La web esta construida con:

- HTML, CSS y JavaScript puro.
- Canvas para renderizar frames del video.
- Seccion sticky de `600vh` para animacion controlada por scroll.
- Precarga de frames con pantalla de carga.
- Renderizado tipo `cover` para que el video llene la pantalla sin deformarse.
- Compatibilidad HiDPI/retina mediante escalado por `devicePixelRatio`.

## Video y frames

Analisis del video original:

- Resolucion: `1280x720`
- FPS: `24`
- Duracion: `8s`
- Frames totales: `192`

Primera extraccion:

- Frames a `640x360`, siguiendo la guia inicial de mitad de resolucion.

Mejora posterior:

- Frames regenerados a `1280x720`.
- Calidad JPEG alta con `-q:v 1`.
- Filtros aplicados con ffmpeg:
  - `lanczos`
  - contraste leve
  - saturacion leve
  - nitidez controlada con `unsharp`

Tambien se genero:

- `video_prueba1_enhanced.mp4`

## Contenido incorporado sobre PATS

Contexto general:

- PATS: Programa de Apoyo al Transporte Subnacional.
- Pertenece al Ministerio de Transportes y Comunicaciones del Peru.
- Ejecutado por Provias Descentralizado.
- Orientado a infraestructura vial rural, inclusion social, competitividad y descentralizacion.

Datos incorporados desde la presentacion:

- Solo `1 de cada 3 hogares` percibia sus caminos vecinales en condicion adecuada para transitar.
- Camino vecinal en condicion adecuada: `33,50%`.
- Red vial vecinal pavimentada en 2018: `1,906.2 km`, equivalente a `1,70%`.
- Red vial vecinal no pavimentada en 2018: `111,886.6 km`, equivalente a `98,30%`.
- Componente I: `139` proyectos de mejoramiento y rehabilitacion.
- Componente I: `2,497 km`.
- Componente I: `S/ 3,019 millones`.
- Componente II: `121` mantenimientos.
- Componente II: `2,448 km`.
- Componente II: `S/ 362 millones`.
- Componente III: `194` Planes Viales Provinciales Participativos.

## Cambios de diseno realizados

### Version inicial

Se creo una landing institucional con:

- Navbar.
- Hero PATS.
- Seccion de programa/componentes.
- Animacion scroll-driven.
- Features de impacto.
- CTA final.
- Footer.

### Mejora de interactividad

Se agrego inicialmente un panel con:

- Barra tipo scrubber.
- Botones de frame anterior/siguiente.
- Bloqueo manual de frame.
- Modo enfoque.

Decision posterior:

- Se retiro esa barra porque no era la direccion deseada.
- La interactividad ahora es narrativa y ocurre naturalmente con el scroll.

### Version actual de interactividad

La seccion de video mantiene:

- Animacion por scroll.
- Indicador de avance visual.
- Metricas principales del tramo activo.
- Etapas narrativas que cambian segun el avance:
  - Diagnostico.
  - Intervencion.
  - Mantenimiento.
  - Gestion vial.

No hay barra manual visible ni controles tipo reproductor.

### Interactividad avanzada sobre el video

Se amplio la experiencia del video para que todo el relato aparezca durante el scroll, usando un solo video de fondo en canvas.

Elementos agregados:

- Seccion de video mas larga para permitir una narrativa por tramos.
- Titular y texto principal dinamicos segun la escena activa.
- Metricas dinamicas que cambian durante el avance.
- Ventanas flotantes sobre el video con cifras clave.
- Marcadores visuales sobre el recorrido.
- Puntos de progreso no interactivos para orientar el avance.
- Seis escenas narrativas:
  - Brecha inicial.
  - Estado de la red vecinal.
  - Mejoramiento y rehabilitacion.
  - Mantenimiento vial.
  - Planes viales provinciales participativos.
  - Cierre institucional PATS.

Decision de interaccion:

- La experiencia sigue siendo scroll-driven.
- No se agregaron controles manuales tipo reproductor.
- Las ventanas aparecen y desaparecen automaticamente segun el porcentaje de scroll dentro del video.

### Rediseño de informacion como 3D Card Fan

Se reemplazaron las ventanas flotantes por un efecto de abanico 3D de cards.

Caracteristicas:

- Cards apiladas con perspectiva 3D.
- Apertura progresiva en forma de abanico durante el scroll.
- Uso de `perspective`, `transform-style: preserve-3d`, `translateZ`, `rotateY` y `rotateZ`.
- Cada card representa una escena o dato clave del PATS.
- La card activa se resalta mientras el resto queda en profundidad.
- El efecto se implemento con CSS y JavaScript puro, sin depender de GSAP, Framer Motion o Three.js.

Cards actuales:

- Diagnostico: `1 de 3`.
- Brecha vial: `98,30%`.
- Componente I: `139` proyectos.
- Componente II: `121` mantenimientos.
- Componente III: `194` PVPP.
- Resultado: PATS como agenda integral.

### Correccion solicitada para el 3D Card Fan

Observacion del usuario:

- Las cartas no deben aparecer antes de llegar al video.
- Las cartas deben aparecer dentro de la seccion del video, sobre el video/canvas sticky.
- La referencia visual deseada es un abanico 3D como la imagen compartida: cartas oscuras, apiladas con perspectiva, rotacion y separacion tipo fan.
- Deben ser solo 4 cartas.
- Cada carta debe representar un componente/informacion principal del PATS.
- Al hacer clic en una carta, debe expandirse para mostrar mas informacion.

Direccion para la siguiente implementacion:

- Reubicar el fan para que viva estrictamente dentro de `#sticky-stage`.
- Ajustar el layout para que el abanico se vea centrado sobre el video, no como tarjetas sueltas.
- Reducir el set a 4 cards.
- Usar un estilo visual mas cercano a la referencia: fondo oscuro/translucido, borde sutil, texto claro, profundidad 3D y hover/click destacado.
- Agregar estado expandido por clic con mas detalle del componente.
- Mantener el video como una sola pieza de fondo y la interaccion principal por scroll.

### Implementacion corregida del 3D Card Fan

Se ajusto el fan de cartas segun la referencia compartida:

- El fan queda dentro del `#sticky-stage`, superpuesto al video/canvas.
- El fan inicia oculto y solo aparece dentro del tramo del video.
- Se redujo a 4 cartas, una por componente PATS.
- Las cartas usan estilo oscuro/translucido, borde sutil y profundidad 3D.
- La apertura del abanico se calcula con el avance del scroll.
- Cada carta es clicable y puede expandirse para mostrar informacion adicional.
- `Escape` cierra una carta expandida.

Cartas implementadas:

- Componente I: Mejoramiento y rehabilitacion.
- Componente II: Mantenimiento vial subnacional.
- Componente III: Planes viales provinciales participativos.
- Componente IV: Gestion y administracion del programa.

## Estado de Git

Repositorio inicializado en esta carpeta.

Commits realizados:

- `c26f140 Initial PATS scroll animation site`
  - Primer estado funcional de la web.
  - Incluye `index.html`, frames, videos y archivos base.

- `d6cf88f Refine PATS narrative from presentation`
  - Retiro de la barra/scrubber.
  - Ajuste de narrativa segun la presentacion PATS.
  - Incorporacion de cifras y problema vial.

- `cc63165 Document PATS project progress`
  - Creacion de esta bitacora.
  - Versionado del PDF de referencia.

## Servidor local

La web debe abrirse por servidor HTTP, no con doble click.

URL usada:

```powershell
http://localhost:8765/index.html
```

Comando recomendado:

```powershell
python -m http.server 8765
```

## Pendientes sugeridos

- Revisar si el video final sera reemplazado por uno de mejor secuencia/calidad.
- Si cambia el video, regenerar `frames/` y ajustar:
  - `TOTAL_FRAMES`
  - `NATIVE_W`
  - `NATIVE_H`
- Evaluar uso de imagenes reales de proyectos del PDF o material institucional en secciones antes/despues.
- Afinar textos con tono oficial si la web se usara en una presentacion formal.
- Revisar rendimiento si se agregan mas frames o resolucion superior a 720p.
