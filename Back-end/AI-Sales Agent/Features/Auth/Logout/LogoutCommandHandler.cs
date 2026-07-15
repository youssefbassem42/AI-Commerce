using AI_Sales_Agent.Abstractions;
using AI_Sales_Agent.Domain;
using AI_Sales_Agent.Infrastructure.Auth;
using MediatR;
using Microsoft.AspNetCore.Identity;

namespace AI_Sales_Agent.Features.Auth.Logout
{
    public class LogoutCommandHandler : IRequestHandler<LogoutCommand, ApiResult>
    {
        private readonly ICurrentUserService _currentUserService;
        private readonly UserManager<User> _userManager;

        public LogoutCommandHandler(ICurrentUserService currentUserService, UserManager<User> userManager)
        {
            _currentUserService = currentUserService;
            _userManager = userManager;
        }

        public async Task<ApiResult> Handle(LogoutCommand request, CancellationToken cancellationToken)
        {
            if (_currentUserService.UserId is not { } userId)
            {
                throw new UnauthorizedAccessException("User is not authenticated.");
            }

            var user = await _userManager.FindByIdAsync(userId.ToString());
            if (user is null)
            {
                throw new UnauthorizedAccessException("User is not authenticated.");
            }

            await _userManager.UpdateSecurityStampAsync(user);
            return ApiResult.Success("Logged out successfully.");
        }
    }
}
