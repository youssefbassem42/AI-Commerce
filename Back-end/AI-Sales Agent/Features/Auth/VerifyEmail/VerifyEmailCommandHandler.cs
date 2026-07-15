using AI_Sales_Agent.Abstractions;
using AI_Sales_Agent.Domain;
using MediatR;
using Microsoft.AspNetCore.Identity;

namespace AI_Sales_Agent.Features.Auth.VerifyEmail
{
    public class VerifyEmailCommandHandler : IRequestHandler<VerifyEmailCommand, ApiResult>
    {
        private readonly UserManager<User> _userManager;

        public VerifyEmailCommandHandler(UserManager<User> userManager)
        {
            _userManager = userManager;
        }

        public async Task<ApiResult> Handle(VerifyEmailCommand request, CancellationToken cancellationToken)
        {
            var user = await _userManager.FindByIdAsync(request.UserId.ToString());
            if (user is null)
            {
                return ApiResult.Failure("Email verification failed.", new[] { "Invalid verification request." });
            }

            var result = await _userManager.ConfirmEmailAsync(user, request.Token);
            if (!result.Succeeded)
            {
                return ApiResult.Failure("Email verification failed.", result.Errors.Select(error => error.Description));
            }

            return ApiResult.Success("Email verified successfully.");
        }
    }
}
