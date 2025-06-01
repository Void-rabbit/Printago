#ifndef MOCKAUTHSERVICE_H
#define MOCKAUTHSERVICE_H

#include "Printago/Agents/IAuthService.h" // Adjusted path
#include <QObject> // For QTimer
#include <QString>

// Forward declare QTimer if only used in .cpp
// class QTimer;

class MockAuthService : public QObject, public IAuthService
{
    Q_OBJECT // Required for QTimer if it's a member or used with signals/slots directly in this class

public:
    explicit MockAuthService(QObject *parent = nullptr);
    ~MockAuthService() override = default;

    void login(
        const QString& email,
        const QString& password,
        std::function<void(bool success, const QString& message)> callback) override;

    void logout() override;
    bool isLoggedIn() const override;
    QString getCurrentUserEmail() const override;

private:
    bool m_isLoggedIn = false;
    QString m_currentUserEmail;
};

#endif // MOCKAUTHSERVICE_H
