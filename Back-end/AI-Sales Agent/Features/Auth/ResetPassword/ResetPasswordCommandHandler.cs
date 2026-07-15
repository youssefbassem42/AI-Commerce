using System.Net;
using System.Text;
using AI_Sales_Agent.Abstractions;
using AI_Sales_Agent.Domain;
using MediatR;
using Microsoft.AspNetCore.WebUtilities;
using Microsoft.AspNetCore.Identity;

namespace AI_Sales_Agent.Features.Auth.ResetPassword
{
    public class ResetPasswordCommandHandler : IRequestHandler<ResetPasswordCommand, ApiResult>
    {
        private readonly UserManager<User> _userManager;

        public ResetPasswordCommandHandler(UserManager<User> userManager)
        {
            _userManager = userManager;
        }

        public async Task<ApiResult> Handle(ResetPasswordCommand request, CancellationToken cancellationToken)
        {
            var user = await _userManager.FindByEmailAsync(request.Email);
            if (user is null)
            {
                return ApiResult.Failure("Password reset failed.", new[] { "Invalid reset request." });
            }

            var token = DecodeResetToken(request.Token);
            var result = await _userManager.ResetPasswordAsync(user, token, request.NewPassword);
            if (!result.Succeeded)
            {
                return ApiResult.Failure("Password reset failed.", result.Errors.Select(error => error.Description));
            }

            await _userManager.UpdateSecurityStampAsync(user);
            return ApiResult.Success("Password reset successfully.");
        }

        private static string DecodeResetToken(string token)
        {
            try
            {
                return Encoding.UTF8.GetString(WebEncoders.Base64UrlDecode(token));
            }
            catch (FormatException)
            {
                return token.Contains('%') ? WebUtility.UrlDecode(token) : token;
            }
        }
    }
}
