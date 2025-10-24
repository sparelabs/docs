# Spare Enterprise

# `DriverDispatchCommunication`

**Feature Flag Type:** Spare Enterprise

**Description:** Enables the Live Messages feature, which allows for real-time, two-way text communication between dispatchers (in the admin panel) and drivers (in the Driver App).

**Why Enable:** This is a fundamental feature for any operation that requires direct communication between dispatch and drivers. It eliminates the need for phone calls or external messaging apps for routine updates, such as clarifying an address, reporting a minor delay, or confirming instructions. It creates a centralized, auditable log of communication.

**Pre-requisites:**
- None.

**Notes:**
- The Live Messages interface is accessible from several places in the admin panel, including the Live Map and the Duty View.
- Is a prerequisite for `QuickReplies`.

**Related Feature Flags:**
- **Required for:** `QuickReplies` (enables one-click pre-defined messages).

---

# `DutyPulloutVisibility`

**Feature Flag Type:** Spare Enterprise

**Description:** Enhances the Live Map by making duty pullouts more visible. It provides clear visual indicators for drivers who are late to start their duty, as well as those who are on time.

**Why Enable:** Provides dispatchers with critical, at-a-glance information about on-time performance. By immediately highlighting late pullouts, dispatchers can proactively contact the driver to resolve the issue, minimizing downstream impacts on the service schedule.

**Pre-requisites:**
- None.

**Notes:**
- This feature adds filters and visual cues to the duties list on the Live Map.

**Related Feature Flags:**
Works independently of other flags.

---

# `DriverInAppCalling`

**Feature Flag Type:** Spare Enterprise

**Description:** Enables a "Call Rider" button within the Driver App, allowing drivers to initiate a phone call to the rider directly from the app. The call is masked to protect both the driver's and the rider's personal phone numbers.

**Why Enable:** Provides a secure and convenient way for drivers to contact riders when needed (e.g., if they can't find the rider at the pickup location). Using masked numbers is a critical privacy feature that prevents the exchange of personal contact information.

**Pre-requisites:**
- Requires a configured Twilio account for voice call masking.

**Notes:**
- The call is initiated through the app, but it is a standard cellular call, not a VoIP call.

**Related Feature Flags:**
Works independently of other flags.

---

# `VehicleInspections`

**Feature Flag Type:** Spare Enterprise

**Description:** Enables the pre- and post-duty vehicle inspection feature. Drivers are required to complete a customizable checklist in the Driver App before starting their duty and/or after ending it.

**Why Enable:** This is a critical feature for fleet maintenance, safety, and compliance. It ensures that vehicles are regularly checked for safety issues or damage, creating a digital record of each inspection. This helps organizations maintain a safe fleet, track vehicle issues, and comply with regulatory requirements.

**Pre-requisites:**
- Requires the creation of at least one Vehicle Inspection Template in the admin panel.

**Notes:**
- Inspection templates are highly customizable, allowing for different checklists for different vehicle types.
- Failed inspection items can trigger alerts to maintenance staff.

**Related Feature Flags:**
Works independently of other flags.

---

# `ViewDriverKpis`

**Feature Flag Type:** Spare Enterprise

**Description:** Displays a "Driver Summary Card" on the driver's detail page in the admin panel. This card shows key performance indicators (KPIs) for the driver, such as on-time performance, completion rate, and other metrics.

**Why Enable:** Provides fleet managers and dispatchers with a quick, data-driven overview of a driver's performance. This helps in identifying high-performing drivers, as well as those who may need additional training or support.

**Pre-requisites:**
- None.

**Notes:**
- The specific KPIs displayed can be configured.

**Related Feature Flags:**
Works independently of other flags.

---

# `OptimizationInsights`

**Feature Flag Type:** Spare Enterprise

**Description:** Enables an experimental "Optimization Insights" page in the Service Planning section of the admin panel. This tool allows service planners to run simulations to see how changes to service parameters (e.g., number of vehicles, service hours) would impact key metrics like cost per trip and trips per hour.

**Why Enable:** This is a powerful tool for data-driven service design. It allows planners to test different scenarios and make informed decisions about service adjustments without impacting the live service. It helps in finding the most efficient and cost-effective service configuration.

**Pre-requisites:**
- Requires historical ridership data to run accurate simulations.

**Notes:**
- This is an experimental feature and the results should be used as a guide, not as a definitive prediction.

**Related Feature Flags:**
Works independently of other flags.

---

# `DemandForecasting`

**Feature Flag Type:** Spare Enterprise

**Description:** DEPRECATED. This feature is no longer in use and should not be enabled. It was intended to show demand forecasting based on historical data.

**Why Enable:** Do not enable. This feature is deprecated due to data inaccuracies.

**Pre-requisites:**
- N/A

**Notes:**
- This feature is not maintained and will be removed in a future release.

**Related Feature Flags:**
- None.

---

# `TripGroup`

**Feature Flag Type:** Spare Enterprise

**Description:** Enables the Trip Groups feature, which allows for the creation of "school bus" or "commuter shuttle" style services. Multiple recurring trips can be bundled together into a single, cohesive group that is assigned to a specific duty or driver.

**Why Enable:** This is essential for organizations that run subscription-based or scheduled services where the same group of riders is transported on a regular basis. It simplifies the management of these complex recurring trips by treating them as a single operational unit.

**Pre-requisites:**
- Requires the use of the Recurring Trips feature.

**Notes:**
- Trip Groups have their own set of validation rules to ensure that all trips within the group are feasible for a single duty.

**Related Feature Flags:**
Works with `RecurringTrips`.

---

# `FleetArea`

**Feature Flag Type:** Spare Enterprise

**Description:** Allows an administrator to attach a specific geographic area (a zone) to a fleet. When a Fleet Area is set, that fleet will only be assigned requests that start or end within its defined area.

**Why Enable:** This is a powerful tool for operations that have multiple fleets serving distinct geographic zones. It enforces operational boundaries and prevents fleets from being assigned trips that are far outside their intended service area, leading to improved efficiency and reduced deadhead mileage.

**Pre-requisites:**
- Requires the creation of zones in the system.

**Notes:**
- Once a Fleet Area is set for a fleet, the restriction is enforced by the engine even if this feature flag is later disabled. The flag simply controls the visibility of the setting in the admin UI.

**Related Feature Flags:**
Works independently of other flags.

---

# `CompleteActivityLog`

**Feature Flag Type:** Spare Enterprise

**Description:** Expands the activity log to show all past events for a request, duty, or rider, rather than being limited to a recent time window (e.g., the last 14 days).

**Why Enable:** This is crucial for organizations that require a complete, long-term audit trail of all actions and system events. It's essential for historical analysis, incident investigation, and compliance with data retention policies that require a full history of events to be accessible.

**Pre-requisites:**
- None.

**Notes:**
- This feature may have performance implications on the activity log for entities with a very large number of historical events.

**Related Feature Flags:**
Works independently of other flags.

---

# `OrganizationPrivacyConfigurations`

**Feature Flag Type:** Spare Enterprise

**Description:** Enables a set of advanced privacy configuration settings for an organization, allowing for more granular control over data privacy and anonymization.

**Why Enable:** For organizations with stringent data privacy requirements, this feature provides the necessary tools to configure the system to meet their specific policies. It allows for a higher level of data protection and compliance.

**Pre-requisites:**
- None.

**Notes:**
- The specific settings enabled by this flag are located in the organization's settings page.

**Related Feature Flags:**
Works independently of other flags.

---

# `DataReconciliation`

**Feature Flag Type:** Spare Enterprise

**Description:** Enables the ability to edit certain metric-related fields on a request *after* it has been completed. This includes fields like pickup and dropoff times, payment method, and rider count.

**Why Enable:** This is a critical tool for data correction and reporting accuracy. If a driver forgot to mark a dropoff as complete at the correct time, or if a payment method needs to be adjusted post-trip, this feature allows an admin to correct the data. This ensures that historical reports and analytics are accurate.

**Pre-requisites:**
- A request must be in the "Completed" status to be editable.

**Notes:**
- All changes made via Data Reconciliation are logged in the activity feed for auditing purposes.

**Related Feature Flags:**
Works independently of other flags.

---

# `FixedRouteTravelDuration`

**Feature Flag Type:** Spare Enterprise

**Description:** When enabled, the system will calculate the "equivalent fixed-route travel duration" for an on-demand trip and include this metric in the ridership report. This calculation is done by querying a third-party routing service (like Google Maps) for the duration of a similar trip on public transit.

**Why Enable:** Provides a powerful data point for comparing the performance of the on-demand service against traditional fixed-route transit. This is valuable for reporting to transit authorities or other stakeholders to demonstrate the efficiency and time savings of the on-demand service.

**Pre-requisites:**
- Requires a configured integration with a third-party routing provider.

**Notes:**
- This is a data-enrichment feature for reporting and does not affect the live operation of the service.
- Can be a prerequisite for `FixedRouteEquivalentDetour`.

**Related Feature Flags:**
- **Required for:** `FixedRouteEquivalentDetour` (uses this calculation to set detour flexibility).

---

# `FixedRouteAlternativesInLaunch`

**Feature Flag Type:** Spare Enterprise

**Description:** Enables the display of fixed-route transit alternatives directly on the estimate page in the admin booking flow. When a dispatcher is booking an on-demand trip, they will also see options for how the rider could make the same trip using public transit, including cost and travel time.

**Why Enable:** Empowers dispatchers and booking agents to provide comprehensive mobility options to riders. If a rider is flexible, the agent can inform them of a potentially cheaper (though likely slower) fixed-route option, promoting the use of the entire public transit network.

**Pre-requisites:**
- Requires a GTFS feed for the fixed-route transit system to be loaded into Spare.

**Notes:**
- This feature is focused on the admin booking experience and does not affect the rider-facing applications.
- `Multimodal` is a related concept, but `FixedRouteAlternativesInLaunch` is specifically about showing these options in the admin booking flow.

**Related Feature Flags:**
- Works with `Multimodal`.

---

# `MultipleWorkflows`

**Feature Flag Type:** Spare Enterprise

**Description:** Removes the default limit of one workflow per organization, allowing administrators to create and manage multiple, distinct workflows.

**Why Enable:** This is essential for organizations that operate different types of services or have different business processes that require unique workflows. For example, an organization might have one workflow for their paratransit service and a completely different one for a microtransit service.

**Pre-requisites:**
- None.

**Notes:**
- Workflows are a powerful tool for automating business processes, and this flag unlocks their full potential for organizations with diverse needs.

**Related Feature Flags:**
Works independently of other flags.

---

# `ConditionalEligibility`

**Feature Flag Type:** Spare Enterprise

**Description:** Enables the ability to define advanced, condition-based eligibility rules for group memberships. These rules can be based on external factors like the current weather, temperature, or special events (via a free-text field).

**Why Enable:** This allows for dynamic, real-time adjustments to service eligibility based on changing conditions. For example, an organization could create a rule that automatically makes a "Severe Weather" rider type eligible for service when the temperature drops below freezing, or enables a "Special Event" group during a festival. This automates what would otherwise be a manual process.

**Pre-requisites:**
- Requires an external data source for weather/temperature information if using those condition types.

**Notes:**
- This is a very powerful feature for creating highly dynamic and responsive services.

**Related Feature Flags:**
Works independently of other flags.

---

# `EditableCaseIdPrefix`

**Feature Flag Type:** Spare Enterprise

**Description:** Allows the prefix for case IDs in Spare Engage to be editable. By default, the prefix is fixed.

**Why Enable:** Provides flexibility for organizations that need to follow a specific case numbering convention, perhaps to align with an external system or for reporting purposes. It allows them to customize the case IDs to fit their internal business processes.

**Pre-requisites:**
- The organization must be using Spare Engage.

**Notes:**
- This is a simple configuration enhancement for case management.

**Related Feature Flags:**
Works independently of other flags.
