# class RandomRateThrottle(BaseThrottle):
#     throttle_scope = 'uploads'
#     scope = 'test'
#     def allow_request(self, request, view):
#         return random.randint(1, 10) != 1
