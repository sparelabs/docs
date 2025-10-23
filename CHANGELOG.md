## 2025-10-17 - Daily Update

# Release Summary - Friday, October 17, 2025

*What's New in Spare*

---

## 🎯 Operations

### ⏱️ Smarter Duty Interruption Handling

**What's New**  
When creating a duty interruption that doesn't fully fit (e.g., due to the duty ending soon), the system will now automatically create a shortened interruption of the maximum possible length. You will receive a specific notification message indicating that the interruption has been shortened.

**Pre-requisites**
- Requires Administrator access

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- *Live Map > select a Duty > Breaks tab > Add Break button*
- *Operations > Duties > select a Duty > Breaks tab > Add Break button*

**What You Can Do**
- Create a duty interruption without worrying if it perfectly fits the remaining schedule.
- If an interruption is too long, the system will automatically adjust it to the maximum allowable duration.
- Receive a notification that clearly states: "The interruption was shortened to fit on the duty." If it cannot be scheduled at all, you will be notified of the failure.

**Why This Matters**  
Previously, creating an interruption that was too long for the remaining duty time would simply fail, forcing manual recalculation. This change prevents failures by creating the longest possible interruption and clearly communicates the adjustment, ensuring drivers get their breaks without extra work for dispatchers.

</details>

---

### 🐛 Bug Fixes

- **Service Estimates Zone Validation (BUS-3786)**
  - _Resolution_: Fixed an issue where a service might not appear as an option during trip planning if the location was within a zone that had time-based service gaps (e.g., no coverage mid-day). The system now validates geography first to show the service, and only validates the selected time when a booking is being finalized.

---

## 📊 Analytics

### 📊 Query Group Membership Custom Fields Directly

**What's New**  
Custom fields attached to Group Memberships are now directly available as dimensions within the `group_membership` cube in Analytics. This allows you to build more detailed reports using group membership data without needing to join through the ridership report.

**Pre-requisites**
- Requires `AnalyticsV2` feature flag

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- *Analytics > Query Builder* (when building a query using the `group_membership` cube).

**What You Can Do**
- Add custom fields from group memberships (e.g., `metadata_eligibility_code`) as dimensions or filters in your reports.
- Analyze rider cohorts based on specific attributes stored in their group membership custom fields.

**Why This Matters**  
Previously, accessing group membership custom fields was limited and required complex workarounds. This change simplifies reporting by making these fields first-class dimensions, enabling easier and more powerful analysis of rider groups based on their specific attributes.

</details>

---

### 🔗 Link Case Data to Admin Details in Reports

**What's New**  
You can now join the `case_data` cube with the `organization_admin` cube in Analytics. This allows you to include details about the assigned administrator (like their first name, last name, or phone number) in reports about cases.

**Pre-requisites**
- Requires `AnalyticsV2` feature flag

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- *Analytics > Query Builder* (when creating a report with `case_data` as a measure or dimension).

**What You Can Do**
- Create reports that show case data alongside the name of the administrator assigned to each case.
- Filter or group cases by the assigned administrator's attributes.

**Why This Matters**  
Before, it was not possible to report on the details of the admin assigned to a case, which limited reporting on agent workload and case distribution. Now you can create reports that show, for example, the number of cases assigned to each administrator, enabling better operational oversight.

</details>

---

### 🐛 Bug Fixes

- **Ridership Report Payment Method Capture (BUS-4303)**
  - _Resolution_: Corrected an issue in the Ridership Report where the `payment_method_type_name` was not being captured for transactions using Cash or Ticket payment methods. These will now appear correctly in reports.

---

## 🤖 AI Voice

### 🗣️ More Robust Date Recognition for Rider Authentication

**What's New**  
AI Voice now more rigorously validates dates of birth provided by callers for authentication. It now rejects ambiguous spoken dates like "one one ninety two" (which could be January 1st or November 1st) while correctly understanding various formats like "June 6th 2025" and "2025 06 01".

**Pre-requisites**
- Requires AI Voice to be enabled for your organization

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- This change affects the backend logic during the rider authentication step of an inbound phone call handled by AI Voice. Callers will experience more accurate authentication.

**What You Can Do**
- Rely on AI Voice to correctly identify riders based on their date of birth, even when provided in different spoken formats.
- Be confident that ambiguous dates will be rejected, prompting the caller for clarification instead of potentially matching with the wrong rider.

**Why This Matters**  
This prevents incorrect authentications caused by ambiguous date formats, improving security and the accuracy of the authentication process. Callers are now correctly prompted for clarification if their spoken date is unclear, ensuring a more reliable experience.

</details>

---

## ⚙️ Admin

### ✈️ Cross-Region Data Migration Tool

**What's New**  
A new interface is available for migrating organization data between different geographic regions (e.g., from a US environment to an EU environment). The tool provides a dedicated UI to select a source and destination organization, choose specific data items to migrate (like services, zones, and riders), and monitor the results.

**Pre-requisites**
- Requires Super admin permissions

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- *Super Admin > Data Migrations* (new page at `/crossRegionDataMigrations`).

**What You Can Do**
- Select a source and destination region and organization for the migration.
- Choose which data categories (e.g., `Service`, `Zone`, `Rider`, `FarePass`) to include in the migration.
- Submit the migration and view a results panel that shows the success or failure status for each item.

**Why This Matters**  
This tool provides a self-serve way for authorized administrators to perform complex cross-region data migrations, which was previously a manual and error-prone engineering task. It streamlines the process of setting up new organizations in different regions.

</details>

---

### 🗺️ Centralized Multimodal Graph Configuration

**What's New**  
The configuration for multimodal graphs (used for journey planning) has been moved and redesigned. It is now located within each organization's settings page, providing a centralized place to manage graphs, datasets, and view build status. A new "Request Rebuild" button allows you to easily trigger a new graph build after updating data.

**Pre-requisites**
- Requires Super admin permissions

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- *Super Admin > Organizations > select an Organization > Multimodal Configuration tab*.

**What You Can Do**
- View the current build status, last build time, and version of the active multimodal graph.
- Click the "Request Rebuild" button to trigger a new build of the graph.
- Manage all datasets (GTFS, Flex, OpenStreetMap) associated with the organization's graph from a single, filtered list.
- Add, create, or edit datasets within the context of the selected organization.

**Why This Matters**  
Previously, managing graph configurations was spread across different pages and was not tied directly to an organization, leading to potential misconfigurations. This new, organization-centric UI simplifies management, reduces errors, and provides clear visibility into the status of each graph.

</details>

---

### 🌐 Set a Default Country for Your Organization

**What's New**  
You can now set a default country for your organization. This country's flag and phone prefix will automatically be selected in phone number input fields across the platform, such as when adding a new rider.

**Pre-requisites**
- Requires Administrator access

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- *Settings > Organization > General section* (new "Default Country" dropdown).

**What You Can Do**
- Select a country from the dropdown to set it as the default for your organization.
- When creating a new rider or editing a phone number, the input field will default to your chosen country's flag and prefix.

**Why This Matters**  
This saves time and reduces errors for administrators in regions outside the US by pre-filling the correct country code, ensuring phone numbers are formatted correctly by default.

</details>

---

### 📸 Enhanced Security for Admin and Driver Photos

**What's New**  
Photo URLs for administrators and drivers are now secured, expiring after a short time to prevent unauthorized access. As part of this security enhancement, the "Photo" column has been removed from the main list views for Drivers and Admins, aligning their behavior with Rider profiles.

**Pre-requisites**
- Requires Administrator access

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- *System > Drivers* (list view table)
- *System > Admins* (list view table)
- Photos remain visible on individual profile pages (e.g., *System > Drivers > [Driver Name]*).

**What You Can Do**
- The "Photo" column is no longer present in the list views for drivers and administrators.
- You can still view, upload, and manage photos by navigating to an individual's profile page.

**Why This Matters**  
This change enhances data privacy and security by ensuring that profile photos cannot be accessed via a permanent, public URL, protecting personal information.

</details>

---

### 🐛 Bug Fixes

- **Group Membership Metadata Preservation (ENG-831)**
  - _Resolution_: Fixed a bug where updating a single metadata field on a group membership via the API would incorrectly erase all other existing metadata. The update process now correctly merges the changes, preserving all other fields.

---

## 🔧 Resolve

### 🐛 Bug Fixes

- **Address Field Headers in Form Viewer (ENG-708)**
  - _Resolution_: Corrected an issue in the form viewer where headers from the address input field (e.g., "Search for an address") were incorrectly appearing in the table of contents on the side panel.

---
_Generated from 23 merged PRs | 12 customer-impacting changes_

---

## 2025-10-17 - Daily Update

# Release Summary - Friday, October 17, 2025

*What's New in Spare*

---
## 🤖 AI Voice

### 🗣️ More Accurate Date of Birth Recognition

**What's New**  
AI Voice is now more precise when handling dates of birth for rider authentication. It is stricter about ambiguous formats and better at understanding various spoken date formats to improve the success rate of voice authentication.

**Pre-requisites**
- Requires AI Voice to be enabled for the organization.

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- This is a non-visual improvement to the background processing of the AI Voice call flow during rider authentication.

**What You Can Do**
- Riders can authenticate using dates like "June 6th 2025" or "2025 06 01," and the system will correctly understand them.
- The system will now reject ambiguous dates like "one one ninety two" (which could be January 1st or November 1st) to prevent incorrect authentications.

**Why This Matters**  
Inaccurate date recognition could lead to failed authentications or, in rare cases, authenticating the wrong rider. This improvement increases the reliability and security of the AI Voice authentication process by correctly handling clear date formats and rejecting ambiguous ones.

</details>

---
## 🎯 Operations

### ⏱️ Smarter Duty Interruption Scheduling

**What's New**  
When creating a duty interruption, the system now intelligently handles situations where the duty is ending soon. If the full interruption doesn't fit, the system will automatically schedule a shorter one if possible and notify you of the change.

**Pre-requisites**
- Requires Administrator access with permissions to manage duties.

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- *Rides > Live Map > (Select a Duty) > Breaks tab > Add Break button*

**What You Can Do**
- When you create an interruption near the end of a duty:
  - If the full duration fits, it will be created as requested.
  - If only a partial duration fits, the interruption will be created for that shorter duration, and a notification will inform you (e.g., "Interruption created but shortened to 15 minutes").
  - If it doesn't fit at all, you'll receive a clear failure message (e.g., "Could not create interruption as there is not enough time remaining in the duty").

**Why This Matters**  
Previously, attempting to create an interruption that didn't fit within the remaining duty time would simply fail without a clear explanation. This enhancement provides better feedback and automatically adjusts the break when possible, creating a more intuitive workflow for dispatchers.

</details>

---
### 🐛 Bug Fixes

- **Service Availability During Fare Estimation (BUS-3786)**
  - _Resolution_: Fixed an issue where some services were not appearing as available during fare estimation due to time-based rules on their service zones. The system now validates geography first to show available services, and applies time validation only after a specific trip time is selected.

---
## 📊 Analytics

### 📊 Query Group Membership Custom Fields

**What's New**  
Custom fields associated with Group Memberships are now directly available for querying in Analytics V2. This allows for building more detailed reports based on custom data stored on group memberships.

**Pre-requisites**
- Requires `AnalyticsV2` feature flag.

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- *Analytics > Query Builder* (when using the `Group Memberships` data source).

**What You Can Do**
- In the Query Builder, select the `Group Memberships` data source.
- You will now see your custom fields (e.g., `metadata_field_name`) available as dimensions for filtering, grouping, and display.

**Why This Matters**  
Previously, accessing group membership custom fields was difficult and limited. This change makes that data a first-class citizen in Analytics, enabling richer reports on rider segments, eligibility, and other custom-tracked attributes.

</details>

---
### 🔗 Link Case Assignees to Admin Details in Reports

**What's New**  
In Analytics V2, you can now join `Case Data` with `Organization Admin` data. This allows you to include details about the assigned administrator (like their name or phone number) in reports about cases.

**Pre-requisites**
- Requires `AnalyticsV2` feature flag.

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- *Analytics > Query Builder*

---

## 2025-10-22 - Daily Update

# Release Summary - Wednesday, October 22, 2025

*What's New in Spare*

---

## ✨ New Features

### Work Order Categories

**What's New**
You can now create and manage custom categories for your work orders within the Enterprise Asset Management (EAM) section. This helps you organize and classify work more effectively.

**Where You'll See It**
You'll find a new "Work Order Categories" section under the "Settings" in the main sidebar. When creating or editing work orders, you'll see a new field to select a category.
- **Requires `EamMfe`**

**What You Can Do**
You can define specific categories like "Vehicle Maintenance," "Facility Repair," or "Safety Check." Then, you can assign these categories to individual work orders, making it easier to filter, sort, and analyze your maintenance tasks.

**Why This Matters**
This feature brings more structure to your work order management, allowing for better reporting and quicker identification of related tasks. It simplifies tracking and ensures your team can easily find and manage work orders based on their type.

---

## 🚀 Feature Enhancements

### Improved Service Discovery for East Bay Paratransit (EBP)

**What's New**
When you're browsing for East Bay Paratransit (EBP) services, the system will now show you all available options, even if the current time falls outside of their regular operating hours. This means you can see the full range of services without being restricted by time.

**Where You'll See It**
This improvement affects how EBP services appear in the service selection dropdown when you are performing a service discovery or estimating a trip.

**What Changed**
- **Before**: If you were looking for an EBP service outside its operating hours (e.g., late at night), it might not have appeared in your search results, even if you were just trying to see what services were available.
- **Now**: All EBP services will be visible during service discovery, regardless of the time you're searching. Time validation will still apply when you actually try to book a trip, ensuring you only book within operating hours.

**Why This Matters**
This enhancement gives you a complete picture of available EBP services at any time, making it easier to plan future trips or understand the full scope of service offerings without being artificially limited by time constraints during your initial search.

### Enhanced Rider Location on Driver App Map

**What's New**
The driver app now displays rider locations with more dynamic and visually engaging markers on the map. These new markers are circular, customizable, and can animate smoothly as the rider moves.

**Where You'll See It**
Drivers will see these enhanced markers on their map within the driver application when a rider is sharing their location.

**What Changed**
- **Before**: Rider location markers were static and less customizable.
- **Now**: Rider locations are shown with modern, customizable circular badges that can include labels, colors, and borders. These markers also animate smoothly when the rider's position updates, providing a more intuitive real-time view.

**Why This Matters**
This update provides drivers with a clearer and more engaging visual representation of rider locations, especially when riders are on the move. The smooth animations help drivers quickly and accurately track their passengers, reducing confusion and improving pickup efficiency.

---

## 🐛 Bug Fixes

-   **Cannot Clear Province/State in Address (ENG-835)** - Previously, when editing an address in a rider's profile, you couldn't clear the "Province/State" or "Country" fields because the "None" option was disabled. Now, you can easily select "None" from the dropdowns to clear these fields, allowing you to completely remove an address if needed.

---

_Generated from 6 merged PRs | 4 customer-impacting changes_

---

