# Salud (Apple Health)

Apple no da acceso a HealthKit desde web/servidor. La vía que funciona:

1. Instala **Health Auto Export** desde el App Store.
2. Configura una exportación automática diaria con los campos: pasos,
   calorías activas, frecuencia cardíaca media.
3. En la app **Atajos**, crea un atajo que se dispare "Cada día a las 23:00"
   (Automatización) y que haga un `POST` a:
   `https://tu-backend.fly.dev/salud/webhook`
   con el JSON que genera Health Auto Export, mapeado a:
   ```json
   { "fecha": "2026-09-03", "pasos": 8500, "calorias_activas": 420, "frecuencia_cardiaca_media": 68 }
   ```
4. Prueba el atajo manualmente una vez y confirma en el dashboard que aparece el dato.

Nota de seguridad: añade una clave secreta en la URL o cabecera antes de
usarlo en producción, para que nadie más pueda escribir en tu endpoint.
