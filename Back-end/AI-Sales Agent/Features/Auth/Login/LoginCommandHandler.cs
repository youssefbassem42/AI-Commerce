using AI_Sales_Agent.Abstractions;
using AI_Sales_Agent.Domain;
using AI_Sales_Agent.Infrastructure.Auth;
using MediatR;
using Microsoft.AspNetCore.Identity;

namespace AI_Sales_Agent.Features.Auth.Login
{
    public class LoginCommandHandler : IRequestHandler<LoginCommand, AuthResult>
    {
        private readonly UserManager<User> _userManager;
        private readonly SignInManager<User> _signInManager;
        private readonly IJwtTokenService _jwtTokenService;

        public LoginCommandHandler(
            UserManager<User> userManager,
            SignInManager<User> signInManager,
            IJwtTokenService jwtTokenService)
        {
            _userManager = userManager;
            _signInManager = signInManager;
            _jwtTokenService = jwtTokenService;
        }

        public async Task<AuthResult> Handle(LoginCommand request, CancellationToken cancellationToken)
        {
            var user = await _userManager.FindByEmailAsync(request.Email);
            if (user is null)
            {
                throw new UnauthorizedAccessException("Invalid email or password.");
            }

            if (!await _userManager.IsEmailConfirmedAsync(user))
            {
                throw new UnauthorizedAccessException("Please verify your email before login.");
            }

            var result = await _signInManager.CheckPasswordSignInAsync(user, request.Password, lockoutOnFailure: true);
            if (!result.Succeeded)
            {
                throw new UnauthorizedAccessException("Invalid email or password.");
            }

            user.LastLogin = DateTime.UtcNow;
            await _userManager.UpdateAsync(user);

            return await _jwtTokenService.CreateTokenAsync(user, cancellationToken);
        }
    }
}
