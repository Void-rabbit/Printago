#include "MockDataService.h"
#include <QDebug>

MockDataService::MockDataService(QObject *parent) : QObject(parent)
{
}

void MockDataService::fetchPrinters(
    std::function<void(bool success, const QList<QVariantMap>& printers, const QString& message)> callback)
{
    QTimer::singleShot(500, this, [callback]() {
        QList<QVariantMap> printers;
        printers << QVariantMap{{"id", "printer1"}, {"name", "Bambu Lab P1S"}, {"status", "Idle"}, {"type", "P1S"}, {"nozzle_temp", 25.0}, {"bed_temp", 30.0}}
                 << QVariantMap{{"id", "printer2"}, {"name", "Bambu Lab X1C"}, {"status", "Printing (75%)"}, {"type", "X1C"}, {"nozzle_temp", 220.0}, {"bed_temp", 55.0}}
                 << QVariantMap{{"id", "printer3"}, {"name", "Prusa MK3S+"}, {"status", "Offline"}, {"type", "MK3S+"}, {"nozzle_temp", 0.0}, {"bed_temp", 0.0}};

        qDebug() << "MockDataService: Fetching printers";
        if (callback) {
            callback(true, printers, "Printers fetched successfully. (Mock)");
        }
    });
}

void MockDataService::fetchPrintJobs(
    std::function<void(bool success, const QList<QVariantMap>& jobs, const QString& message)> callback)
{
    QTimer::singleShot(500, this, [callback]() {
        QList<QVariantMap> jobs;
        jobs << QVariantMap{{"id", "job1"}, {"name", "XYZ_Calibration_Cube.gcode"}, {"status", "Printing (30%)"}, {"printer_id", "printer2"}, {"filament_type", "PLA"}, {"time_elapsed", "10m"}, {"time_remaining", "20m"}}
             << QVariantMap{{"id", "job2"}, {"name", "Benchy_ABS.gcode"}, {"status", "Queued"}, {"printer_id", "printer1"}, {"filament_type", "ABS"}, {"time_elapsed", "0m"}, {"time_remaining", "45m"}}
             << QVariantMap{{"id", "job3"}, {"name", "Voron_Stealthburner_Front.3mf"}, {"status", "Completed"}, {"printer_id", "printer2"}, {"filament_type", "PETG"}, {"time_elapsed", "2h 15m"}, {"time_remaining", "0m"}}
             << QVariantMap{{"id", "job4"}, {"name", "Articulated_Dragon.gcode"}, {"status", "Failed (Spaghetti)"}, {"printer_id", "printer1"}, {"filament_type", "Silk PLA"}, {"time_elapsed", "30m"}, {"time_remaining", "N/A"}};

        qDebug() << "MockDataService: Fetching print jobs";
        if (callback) {
            callback(true, jobs, "Print jobs fetched successfully. (Mock)");
        }
    });
}

void MockDataService::fetchParts(
    std::function<void(bool success, const QList<QVariantMap>& parts, const QString& message)> callback)
{
    QTimer::singleShot(500, this, [callback]() {
        QList<QVariantMap> parts;
        parts << QVariantMap{{"id", "part1"}, {"name", "Benchy.stl"}, {"material", "PLA"}, {"print_time_estimate", "1h 15m"}}
              << QVariantMap{{"id", "part2"}, {"name", "CalibrationCube.3mf"}, {"material", "Any"}, {"print_time_estimate", "20m"}}
              << QVariantMap{{"id", "part3"}, {"name", "PhoneStand_v2.step"}, {"material", "PETG"}, {"print_time_estimate", "2h 30m"}};

        qDebug() << "MockDataService: Fetching parts";
        if (callback) {
            callback(true, parts, "Parts fetched successfully. (Mock)");
        }
    });
}

void MockDataService::fetchProfiles(
    std::function<void(bool success, const QList<QVariantMap>& profiles, const QString& message)> callback)
{
    QTimer::singleShot(500, this, [callback]() {
        QList<QVariantMap> profiles;
        profiles << QVariantMap{{"id", "profile1"}, {"name", "PLA - 0.2mm Standard Quality"}, {"material", "PLA"}, {"layer_height", "0.2mm"}, {"nozzle", "0.4mm"}}
                 << QVariantMap{{"id", "profile2"}, {"name", "PETG - 0.28mm High Speed (0.6mm Nozzle)"}, {"material", "PETG"}, {"layer_height", "0.28mm"}, {"nozzle", "0.6mm"}}
                 << QVariantMap{{"id", "profile3"}, {"name", "ABS - 0.16mm Engineering"}, {"material", "ABS"}, {"layer_height", "0.16mm"}, {"nozzle", "0.4mm"}};

        qDebug() << "MockDataService: Fetching profiles";
        if (callback) {
            callback(true, profiles, "Profiles fetched successfully. (Mock)");
        }
    });
}
