#ifndef ICAMERASERVICE_H
#define ICAMERASERVICE_H

#include <QString>
#include <functional>

// Forward declaration for QWidget to avoid including the full header here
class QWidget;

class ICameraService
{
public:
    virtual ~ICameraService() = default;

    // Returns a widget that will render the camera feed.
    // Ownership of the returned QWidget is typically managed by the ICameraService implementation
    // or it could be parented to a widget provided by the caller.
    // For this iteration, the service will manage it, but CameraFeedPage will handle adding/removing it.
    virtual QWidget* getCameraFeedWidget(const QString& printerId) = 0;

    virtual void startCameraFeed(
        const QString& printerId,
        std::function<void(bool success, const QString& message)> callback) = 0;

    virtual void stopCameraFeed(const QString& printerId) = 0;
};

#endif // ICAMERASERVICE_H
