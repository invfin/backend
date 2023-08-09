class RecommenderMixin:
    generate_recommendations: bool = False
    path_name: str = ""
    recsys_title: str = "Recomendaciones"

    def generate_recsys_path(self):
        return {"recsys_path": f"recsys:{self.path_name}"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"recsys_path": f"recsys:{self.path_name}", "recsys_title": self.recsys_title}
        )
        return context
