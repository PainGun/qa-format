class TareaQAController:
    def __init__(self):
        # Simulación de datos para demo
        self.tarea = {
            'titulo': 'QA Pull Request #1234',
            'autor': 'Juan Pérez',
            'fecha': '2024-06-10',
            'ambiente': 'Staging',
            'prs': ['#1234', '#1235'],
            'comentarios': 'Todo funciona correctamente. Listo para producción.',
            'responsables': {
                'usabilidad': 'Ana UX',
                'código': 'Carlos Dev'
            },
            'resumen': 'Se validaron todos los criterios de aceptación y no se encontraron bugs.'
        }

    def generar_texto(self):
        t = self.tarea
        return (
            f"*📝 QA Reporte Profesional*
"
            f"*Título:* `{t['titulo']}`\n"
            f"*Autor:* `{t['autor']}`\n"
            f"*Fecha:* `{t['fecha']}`\n"
            f"*Ambiente:* `{t['ambiente']}`\n"
            f"*Pull Requests:* {', '.join(f'`{pr}`' for pr in t['prs'])}\n"
            f"*Responsables:*\n    ├─ 👤 Usabilidad: `{t['responsables']['usabilidad']}`\n    └─ 👨‍💻 Código: `{t['responsables']['código']}`\n"
            f"*Comentarios:*\n> {t['comentarios']}\n"
            f"*Resumen:*\n```
{t['resumen']}
```\n"
            f"*Estado:* :white_check_mark: _Aprobado para merge_\n"
        )

    def ejemplo(self):
        return "Controlador funcionando" 