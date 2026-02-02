from warehouse.db_router import set_company

class CompanyMiddleware:
    """
    Show company selection popup if user has not selected a company yet.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set DB for current request
        company_code = request.session.get("company_code")
        if company_code:
            set_company(company_code)
        else:
            set_company("default")

        # Show popup if user has not selected company yet
        request.show_company_popup = "company_code" not in request.session

        response = self.get_response(request)
        return response
