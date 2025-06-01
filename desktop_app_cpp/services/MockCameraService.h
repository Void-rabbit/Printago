#ifndef MOCKCAMERASERVICE_H
#define MOCKCAMERASERVICE_H

#include "Printago/Agents/ICameraService.h" // Adjusted for INCLUDEPATH
#include <QObject>
#include <QMap>
#include <QString>

// Forward declarations
class QLabel;
class QTimer; // QTimer is used for QTimer::singleShot, can be forward declared if only in .cpp

class MockCameraService : public QObject, public ICameraService
{
    Q_OBJECT

public:
    explicit MockCameraService(QObject *parent = nullptr);
    ~MockCameraService() override; // Declare destructor to clean up widgets

    QWidget* getCameraFeedWidget(const QString& printerId) override;

    void startCameraFeed(
        const QString& printerId,
        std::function<void(bool success, const QString& message)> callback) override;

    void stopCameraFeed(const QString& printerId) override;

private:
    QMap<QString, QLabel*> m_mockFeedWidgets;
};

#endif // MOCKCAMERASERVICE_H
