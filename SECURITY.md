# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Considerations

### File Storage
- Downloaded files are stored in the `downloads/` directory
- Files are automatically deleted after 24 hours
- No permanent storage of user data

### Input Validation
- All YouTube URLs are validated before processing
- Command injection protection through yt-dlp's built-in security
- File size limits to prevent disk space abuse

### Network Security
- CORS is configured for localhost only
- No external network access required
- All API endpoints are local

### Data Privacy
- No user authentication or personal data collection
- No logging of user activities
- Temporary job storage only

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **DO NOT** create a public GitHub issue
2. Email security concerns to: [your-email@example.com]
3. Include detailed steps to reproduce
4. Allow 90 days for response before public disclosure

## Security Best Practices

### For Users
- Only run on trusted networks
- Keep yt-dlp updated
- Monitor disk space usage
- Use firewall rules if needed

### For Developers
- Never commit API keys or secrets
- Use environment variables for configuration
- Regular security audits
- Keep dependencies updated

## Known Limitations

- No user authentication
- No rate limiting (relies on system resources)
- No encryption of downloaded files
- No audit logging

## Recommendations

- Run behind a reverse proxy for production
- Implement proper authentication for multi-user environments
- Add rate limiting for public deployments
- Consider file encryption for sensitive content

