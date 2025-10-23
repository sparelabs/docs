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

