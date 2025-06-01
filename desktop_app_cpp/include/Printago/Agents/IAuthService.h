#ifndef IAUTHSERVICE_H
#define IAUTHSERVICE_H

#include <QString>
#include <functional>

class IAuthService
{
public:
    virtual ~IAuthService() = default;

    virtual void login(
        const QString& email,
        const QString& password,
        std::function<void(bool success, const QString& message)> callback) = 0;

    virtual void logout() = 0;
    virtual bool isLoggedIn() const = 0;
    virtual QString getCurrentUserEmail() const = 0;
};

#endif // IAUTHSERVICE_H
