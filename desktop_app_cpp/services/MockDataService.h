#ifndef MOCKDATASERVICE_H
#define MOCKDATASERVICE_H

#include "Printago/Agents/IDataService.h" // Adjusted for INCLUDEPATH
#include <QObject>
#include <QTimer> // For QTimer::singleShot, include fully here or forward declare and include in .cpp

class MockDataService : public QObject, public IDataService
{
    Q_OBJECT

public:
    explicit MockDataService(QObject *parent = nullptr);
    ~MockDataService() override = default;

    void fetchPrinters(
        std::function<void(bool success, const QList<QVariantMap>& printers, const QString& message)> callback) override;

    void fetchPrintJobs(
        std::function<void(bool success, const QList<QVariantMap>& jobs, const QString& message)> callback) override;

    void fetchParts(
        std::function<void(bool success, const QList<QVariantMap>& parts, const QString& message)> callback) override;

    void fetchProfiles(
        std::function<void(bool success, const QList<QVariantMap>& profiles, const QString& message)> callback) override;
};

#endif // MOCKDATASERVICE_H
