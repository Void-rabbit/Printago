#include "settingspage.h"

#include <QLabel>
#include <QListWidget>
#include <QListWidgetItem>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QTabWidget>
#include <QFont> // For styling titles
#include <QDebug> // For messages

#include "Printago/Agents/IDataService.h" // Full include

SettingsPage::SettingsPage(IDataService* dataService, QWidget *parent)
    : QWidget(parent), m_dataService(dataService)
{
    Q_ASSERT(m_dataService != nullptr);
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setAlignment(Qt::AlignTop);

    QLabel *pageTitleLabel = new QLabel("Application Settings", this);
    QFont pageTitleFont = pageTitleLabel->font();
    pageTitleFont.setPointSize(18); // Larger title for the whole page
    pageTitleFont.setBold(true);
    pageTitleLabel->setFont(pageTitleFont);
    pageTitleLabel->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(pageTitleLabel);
    mainLayout->addSpacing(15);


    tabWidget = new QTabWidget(this);

    partsTab = createPartsTab();
    profilesTab = createProfilesTab();

    tabWidget->addTab(partsTab, "Manage Parts");
    tabWidget->addTab(profilesTab, "Manage Print Profiles");

    mainLayout->addWidget(tabWidget, 1); // Allow tab widget to stretch

    setLayout(mainLayout);
}

QWidget* SettingsPage::createPartsTab()
{
    QWidget *widget = new QWidget();
    QVBoxLayout *layout = new QVBoxLayout(widget);
    layout->setAlignment(Qt::AlignTop);

    QLabel *titleLabel = new QLabel("Parts Management", widget);
    QFont tabTitleFont = titleLabel->font();
    tabTitleFont.setPointSize(14);
    tabTitleFont.setBold(true);
    titleLabel->setFont(tabTitleFont);
    titleLabel->setAlignment(Qt::AlignCenter);
    layout->addWidget(titleLabel);
    layout->addSpacing(10);

    partsListWidget = new QListWidget(widget);
    layout->addWidget(partsListWidget, 1); // List takes available vertical space

    QHBoxLayout *buttonLayout = new QHBoxLayout();
    addPartButton = new QPushButton("Add Part", widget);
    editPartButton = new QPushButton("Edit Selected", widget);
    deletePartButton = new QPushButton("Delete Selected", widget);
    // Connect buttons to refreshParts for now as placeholder for actual CRUD
    connect(addPartButton, &QPushButton::clicked, this, &SettingsPage::refreshParts);
    connect(editPartButton, &QPushButton::clicked, this, &SettingsPage::refreshParts);
    connect(deletePartButton, &QPushButton::clicked, this, &SettingsPage::refreshParts);


    buttonLayout->addWidget(addPartButton);
    buttonLayout->addSpacing(10);
    buttonLayout->addWidget(editPartButton);
    buttonLayout->addSpacing(10);
    buttonLayout->addWidget(deletePartButton);
    buttonLayout->addStretch(); // Push buttons to the left
    layout->addLayout(buttonLayout);

    // Initially disable edit/delete buttons, enable on selection
    editPartButton->setEnabled(false);
    deletePartButton->setEnabled(false);
    connect(partsListWidget, &QListWidget::itemSelectionChanged, [this]() {
        bool selected = !partsListWidget->selectedItems().isEmpty();
        editPartButton->setEnabled(selected);
        deletePartButton->setEnabled(selected);
    });


    refreshParts(); // Load data after UI setup
    widget->setLayout(layout);
    return widget;
}

void SettingsPage::refreshParts()
{
    if (!m_dataService) {
        qWarning("SettingsPage (Parts): Data service not available.");
        if(partsListWidget) {
             partsListWidget->clear();
             partsListWidget->addItem("Error: Data service unavailable.");
        }
        return;
    }
    // if(partsListWidget) partsListWidget->addItem("Loading parts..."); // Optional

    m_dataService->fetchParts(
        [this](bool success, const QList<QVariantMap>& parts, const QString& message) {
            if (!partsListWidget) return;
            partsListWidget->clear();
            if (success) {
                if (parts.isEmpty()) {
                    partsListWidget->addItem("No parts found.");
                } else {
                    for (const QVariantMap& partMap : parts) {
                        partsListWidget->addItem(partMap["name"].toString());
                    }
                }
                qDebug() << "SettingsPage (Parts): Loaded -" << message;
            } else {
                partsListWidget->addItem(QString("Failed to load parts: %1").arg(message));
                qWarning() << "SettingsPage (Parts): Failed -" << message;
            }
        });
}

QWidget* SettingsPage::createProfilesTab()
{
    QWidget *widget = new QWidget();
    QVBoxLayout *layout = new QVBoxLayout(widget);
    layout->setAlignment(Qt::AlignTop);

    QLabel *titleLabel = new QLabel("Print Profiles Management", widget);
    QFont tabTitleFont = titleLabel->font();
    tabTitleFont.setPointSize(14);
    tabTitleFont.setBold(true);
    titleLabel->setFont(tabTitleFont);
    titleLabel->setAlignment(Qt::AlignCenter);
    layout->addWidget(titleLabel);
    layout->addSpacing(10);

    profilesListWidget = new QListWidget(widget);
    layout->addWidget(profilesListWidget, 1);

    QHBoxLayout *buttonLayout = new QHBoxLayout();
    addProfileButton = new QPushButton("Add Profile", widget);
    editProfileButton = new QPushButton("Edit Selected", widget);
    deleteProfileButton = new QPushButton("Delete Selected", widget);
    // Connect buttons to refreshProfiles for now
    connect(addProfileButton, &QPushButton::clicked, this, &SettingsPage::refreshProfiles);
    connect(editProfileButton, &QPushButton::clicked, this, &SettingsPage::refreshProfiles);
    connect(deleteProfileButton, &QPushButton::clicked, this, &SettingsPage::refreshProfiles);

    buttonLayout->addWidget(addProfileButton);
    buttonLayout->addSpacing(10);
    buttonLayout->addWidget(editProfileButton);
    buttonLayout->addSpacing(10);
    buttonLayout->addWidget(deleteProfileButton);
    buttonLayout->addStretch();
    layout->addLayout(buttonLayout);

    // Initially disable edit/delete buttons, enable on selection
    editProfileButton->setEnabled(false);
    deleteProfileButton->setEnabled(false);
    connect(profilesListWidget, &QListWidget::itemSelectionChanged, [this]() {
        bool selected = !profilesListWidget->selectedItems().isEmpty();
        editProfileButton->setEnabled(selected);
        deleteProfileButton->setEnabled(selected);
    });

    refreshProfiles(); // Load data after UI setup
    widget->setLayout(layout);
    return widget;
}

void SettingsPage::refreshProfiles()
{
    if (!m_dataService) {
        qWarning("SettingsPage (Profiles): Data service not available.");
        if(profilesListWidget) {
            profilesListWidget->clear();
            profilesListWidget->addItem("Error: Data service unavailable.");
        }
        return;
    }
    // if(profilesListWidget) profilesListWidget->addItem("Loading profiles..."); // Optional

    m_dataService->fetchProfiles(
        [this](bool success, const QList<QVariantMap>& profiles, const QString& message) {
            if(!profilesListWidget) return;
            profilesListWidget->clear();
            if (success) {
                if (profiles.isEmpty()) {
                    profilesListWidget->addItem("No profiles found.");
                } else {
                    for (const QVariantMap& profileMap : profiles) {
                        profilesListWidget->addItem(profileMap["name"].toString());
                    }
                }
                qDebug() << "SettingsPage (Profiles): Loaded -" << message;
            } else {
                profilesListWidget->addItem(QString("Failed to load profiles: %1").arg(message));
                qWarning() << "SettingsPage (Profiles): Failed -" << message;
            }
        });
}
