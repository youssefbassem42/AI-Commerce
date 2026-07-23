using FluentValidation;

namespace AI_Sales_Agent.Infrastructure.Errors
{
    public class ExceptionHandlingMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<ExceptionHandlingMiddleware> _logger;

        public ExceptionHandlingMiddleware(RequestDelegate next, ILogger<ExceptionHandlingMiddleware> logger)
        {
            _next = next;
            _logger = logger;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            try
            {
                await _next(context);
            }
            catch (ValidationException exception)
            {
                context.Response.StatusCode = StatusCodes.Status400BadRequest;
                await context.Response.WriteAsJsonAsync(new
                {
                    message = "Validation failed.",
                    errors = exception.Errors.Select(error => error.ErrorMessage)
                });
            }
            catch (UnauthorizedAccessException exception)
            {
                context.Response.StatusCode = StatusCodes.Status401Unauthorized;
                await context.Response.WriteAsJsonAsync(new
                {
                    message = exception.Message
                });
            }
            catch (Exception exception)
            {
                _logger.LogError(exception, "Unhandled exception.");
                context.Response.StatusCode = StatusCodes.Status500InternalServerError;
                await context.Response.WriteAsJsonAsync(new
                {
                    message = "An unexpected error occurred."
                });
            }
        }
    }
}
