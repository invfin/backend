from model_bakery import baker

from apps.users.tests.factories import regular_user

from apps.seo.models import (
BaseModelVisited,
BaseUserModelVisited,
BaseVisiteurModelVisited,
Journey,
MetaParameters,
MetaParametersHistorial,
UserCompanyVisited,
UserJourney,
UserPublicBlogVisited,
UserQuestionVisited,
UserTermVisited,
Visiteur,
VisiteurCompanyVisited,
VisiteurJourney,
VisiteurPublicBlogVisited,
VisiteurQuestionVisited,
VisiteurTermVisited,
VisiteurUserRelation,
)


baker.make(BaseModelVisited)
baker.make(BaseUserModelVisited)
baker.make(BaseVisiteurModelVisited)
baker.make(Journey)
baker.make(MetaParameters)
baker.make(MetaParametersHistorial)
baker.make(UserCompanyVisited)
baker.make(UserJourney)
baker.make(UserPublicBlogVisited)
baker.make(UserQuestionVisited)
baker.make(UserTermVisited)
baker.make(Visiteur)
baker.make(VisiteurCompanyVisited)
baker.make(VisiteurJourney)
baker.make(VisiteurPublicBlogVisited)
baker.make(VisiteurQuestionVisited)
baker.make(VisiteurTermVisited)
baker.make(VisiteurUserRelation)