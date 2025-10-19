import re
from datetime import datetime, time

def is_email(value):
    return re.match(r"^[^@]+@[^@]+\.[^@]+$", value) is not None

def is_phone(value):
    return re.match(r"^\+?\d{7,15}$", value) is not None

def check_caregiver_availability(caregiver, requested_date, requested_time_start, requested_time_end):
    """
    Check if a caregiver is available for a specific date and time range.
    
    Args:
        caregiver: Caretaker object from the database
        requested_date: Date object for the requested service
        requested_time_start: Time object for the start of requested service
        requested_time_end: Time object for the end of requested service
    
    Returns:
        dict: {
            'available': bool,
            'message': str,
            'conflicts': list of conflicting requests (if any)
        }
    """
    if not caregiver:
        return {
            'available': False,
            'message': 'Caregiver not found',
            'conflicts': []
        }
    
    # Check if caregiver's working hours match the requested time
    if hasattr(caregiver, 'working_hours_start') and hasattr(caregiver, 'working_hours_end'):
        if requested_time_start < caregiver.working_hours_start or requested_time_end > caregiver.working_hours_end:
            return {
                'available': False,
                'message': f'Requested time outside caregiver working hours ({caregiver.working_hours_start} - {caregiver.working_hours_end})',
                'conflicts': []
            }
    
    # Check for conflicting requests on the same date
    conflicts = []
    if hasattr(caregiver, 'requests'):
        for request in caregiver.requests:
            # Check if request is on the same date and status is accepted/pending
            if (hasattr(request, 'date') and request.date == requested_date and 
                hasattr(request, 'status') and request.status in ['accepted', 'pending']):
                
                # Check for time overlap
                if (hasattr(request, 'time_start') and hasattr(request, 'time_end')):
                    if not (requested_time_end <= request.time_start or requested_time_start >= request.time_end):
                        conflicts.append({
                            'request_id': request.id if hasattr(request, 'id') else None,
                            'time_start': str(request.time_start),
                            'time_end': str(request.time_end),
                            'status': request.status
                        })
    
    if conflicts:
        return {
            'available': False,
            'message': f'Caregiver has {len(conflicts)} conflicting request(s) on this date',
            'conflicts': conflicts
        }
    
    return {
        'available': True,
        'message': 'Caregiver is available for the requested time slot',
        'conflicts': []
    }

def get_available_caregivers(all_caregivers, requested_date, requested_time_start, requested_time_end):
    """
    Filter and return a list of available caregivers for a specific date and time.
    
    Args:
        all_caregivers: List of Caretaker objects
        requested_date: Date object for the requested service
        requested_time_start: Time object for the start of requested service
        requested_time_end: Time object for the end of requested service
    
    Returns:
        list: List of available caregiver objects
    """
    available_caregivers = []
    
    for caregiver in all_caregivers:
        availability = check_caregiver_availability(
            caregiver, 
            requested_date, 
            requested_time_start, 
            requested_time_end
        )
        
        if availability['available']:
            available_caregivers.append(caregiver)
    
    return available_caregivers
