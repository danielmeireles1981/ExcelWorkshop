from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

from core.pdf import build_materials_context, resolve_static_base_url


class Command(BaseCommand):
    help = "Gera PDF consolidado com todo o material das fases."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default="material-completo.pdf",
            help="Caminho/nome do arquivo de saida.",
        )

    def handle(self, *args, **options):
        try:
            from weasyprint import HTML  # import lazily para evitar erro de deps no import do comando
        except (ImportError, OSError) as exc:
            raise CommandError(
                "WeasyPrint nao conseguiu carregar as dependencias do sistema. "
                "Instale o runtime do GTK/Pango conforme a documentacao oficial: "
                "https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows "
                f"(detalhes: {exc})"
            )

        output_path = Path(options["output"]).resolve()
        static_base_url = resolve_static_base_url()
        context = build_materials_context(static_base_url=static_base_url)
        html = render_to_string("materials_pdf.html", context)
        pdf_bytes = HTML(string=html, base_url=static_base_url).write_pdf()
        output_path.write_bytes(pdf_bytes)
        self.stdout.write(self.style.SUCCESS(f"PDF gerado em {output_path}"))
