# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** open a public issue
2. Email the maintainer or use GitHub's private vulnerability reporting
3. Include a description of the vulnerability and steps to reproduce

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | Yes       |

## Security Best Practices

When using this API:

- **Never commit your `.env` file** or API keys to version control
- **Use unique API keys** for each application
- **Enable rate limiting** to prevent abuse
- **Run behind a reverse proxy** (nginx/Caddy) in production
- **Use HTTPS** in production environments
