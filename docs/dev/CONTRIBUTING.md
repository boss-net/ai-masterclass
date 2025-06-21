# Contributing to BossKit

Thanks for your interest in contributing to BossKit! Here's how you can get started.

## How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where possible
- Write clear and concise docstrings
- Keep lines under 80 characters
- Use conventional commit messages:
  - `feat`: New features
  - `fix`: Bug fixes
  - `docs`: Documentation changes
  - `style`: Formatting changes
  - `refactor`: Code changes that neither fix a bug nor add a feature
  - `perf`: Performance improvements
  - `test`: Adding missing tests
  - `chore`: Changes to the build process or auxiliary tools

## Testing

Before submitting a PR, please:
1. Run all tests: `make test`
2. Check code coverage: `make coverage`
3. Run linters: `make lint`
4. Run type checking: `make type-check`

## Documentation

- Update relevant documentation for new features
- Add examples where appropriate
- Keep API documentation up to date

## Security

If you discover a security vulnerability, please do not open an issue. Instead, email security@boss-net.com with the details.

## License

By contributing to BossKit, you agree that your contributions will be licensed under the Apache License 2.0.
