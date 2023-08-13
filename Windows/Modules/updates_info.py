#!/usr/bin/env python3

# Libraries
##############################################################################
import win32com.client
import logging
##############################################################################

# Get Update History
##############################################################################
def get_update_history():
    """
    List History of Windows updates.
    """
    update_history = []

    try:
        update_session = win32com.client.Dispatch("Microsoft.Update.Session")
        update_searcher = update_session.CreateUpdateSearcher()

        search_result = update_searcher.QueryHistory(
            0, update_searcher.GetTotalHistoryCount()
        )

        for update in search_result:
            update_info = {
                'title': update.Title,
                'description': update.Description,
                'operation': update.Operation,
                'result_code': update.ResultCode,
                'date': update.Date.strftime('%Y-%m-%d %H:%M:%S'),
            }
            update_history.append(update_info)
    except Exception as e:
        # Log the error
        logging.error(e)

    return update_history
##############################################################################


# Check Missing Updates
##############################################################################
def check_missing_updates():
    """
    Check for missing Windows updates.
    """
    missing_updates = []

    try:
        update_session = win32com.client.Dispatch("Microsoft.Update.Session")
        update_searcher = update_session.CreateUpdateSearcher()

        # Search for updates
        search_result = update_searcher.Search("IsInstalled=0")

        for update in search_result.Updates:
            missing_update = {
                'title': update.Title,
                'description': update.Description,
                'category': update.Categories[0].Name if update.Categories else 'Uncategorized'
            }
            missing_updates.append(missing_update)
    except Exception as e:
        # Log the error
        logging.error(e)

    return missing_updates
##############################################################################


# Categorize Updates
##############################################################################
def categorize_updates(updates):
    """
    Categorize the list of updates based on their classification.
    """
    categorized_updates = {}

    for update in updates:
        if update['category'] not in categorized_updates:
            categorized_updates[update['category']] = []
        categorized_updates[update['category']].append(update)

    return categorized_updates
##############################################################################