#include "dashboardpage.h"

#include <QLabel>
#include <QListWidget>
#include <QListWidgetItem>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QSpacerItem> // For the spacer item
#include <QDebug> // For messages

#include "Printago/Agents/IDataService.h" // Full include for usage

DashboardPage::DashboardPage(IDataService* dataService, QWidget *parent)
    : QWidget(parent), m_dataService(dataService)
{
    Q_ASSERT(m_dataService != nullptr);
    QVBoxLayout *mainLayout = new QVBoxLayout(this);

    // Title
    titleLabel = new QLabel("Printers Overview", this);
    QFont titleFont = titleLabel->font();
    titleFont.setPointSize(16); // Make font larger
    titleFont.setBold(true);
    titleLabel->setFont(titleFont);
    titleLabel->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(titleLabel);

    // Refresh button layout
    QHBoxLayout *buttonLayout = new QHBoxLayout();
    refreshButton = new QPushButton("Refresh Printer List", this);
    connect(refreshButton, &QPushButton::clicked, this, &DashboardPage::refreshPrinters); // Connect button to slot

    buttonLayout->addSpacerItem(new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum)); // Spacer
    buttonLayout->addWidget(refreshButton);
    mainLayout->addLayout(buttonLayout);

    // Printer list
    printerListWidget = new QListWidget(this);
    mainLayout->addWidget(printerListWidget);

    // Initial load of printers
    refreshPrinters();

    setLayout(mainLayout);
}

void DashboardPage::refreshPrinters()
{
    if (!m_dataService) {
        qWarning("DashboardPage: Data service is not available.");
        printerListWidget->clear();
        printerListWidget->addItem("Error: Data service unavailable.");
        return;
    }

    // Optional: Add a loading state to the list
    // printerListWidget->clear();
    // printerListWidget->addItem("Loading printers...");

    m_dataService->fetchPrinters(
        [this](bool success, const QList<QVariantMap>& printers, const QString& message) {
            printerListWidget->clear(); // Clear previous items or loading message
            if (success) {
                if (printers.isEmpty()) {
                    printerListWidget->addItem("No printers found.");
                } else {
                    for (const QVariantMap& printerMap : printers) {
                        QString itemText = QString("%1 - %2")
                                               .arg(printerMap["name"].toString())
                                               .arg(printerMap["status"].toString());
                        QListWidgetItem* item = new QListWidgetItem(itemText);
                        // You can store the full map or ID in the item's data role if needed later
                        // item->setData(Qt::UserRole, printerMap["id"].toString());
                        if (printerMap["status"].toString().contains("Offline", Qt::CaseInsensitive)) {
                            item->setForeground(Qt::gray);
                        } else if (printerMap["status"].toString().contains("Error", Qt::CaseInsensitive)) {
                            item->setForeground(Qt::red);
                        }
                        printerListWidget->addItem(item);
                    }
                }
                qDebug() << "DashboardPage: Printers loaded -" << message;
            } else {
                printerListWidget->addItem(QString("Failed to load printers: %1").arg(message));
                qWarning() << "DashboardPage: Failed to load printers -" << message;
            }
        });
}
