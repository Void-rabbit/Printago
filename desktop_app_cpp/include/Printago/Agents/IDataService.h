#ifndef IDATASERVICE_H
#define IDATASERVICE_H

#include <QString>
#include <QList>
#include <QVariantMap>
#include <functional>

class IDataService
{
public:
    virtual ~IDataService() = default;

    virtual void fetchPrinters(
        std::function<void(bool success, const QList<QVariantMap>& printers, const QString& message)> callback) = 0;

    virtual void fetchPrintJobs(
        std::function<void(bool success, const QList<QVariantMap>& jobs, const QString& message)> callback) = 0;

    virtual void fetchParts(
        std::function<void(bool success, const QList<QVariantMap>& parts, const QString& message)> callback) = 0;

    virtual void fetchProfiles(
        std::function<void(bool success, const QList<QVariantMap>& profiles, const QString& message)> callback) = 0;
};

#endif // IDATASERVICE_H
