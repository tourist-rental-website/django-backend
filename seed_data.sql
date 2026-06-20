-- ============================================================
-- SEED DATA for Travel Platform
-- Run with: psql -U postgres -d <your_db_name> -f seed_data.sql
-- ============================================================

BEGIN;

-- ============================================================
-- 1. USERS (accounts_user)
-- Roles: traveler, guide, hotel, admin
-- Passwords are Django's PBKDF2 hash of "Password123!"
-- ============================================================

INSERT INTO public.accounts_user (id, password, last_login, is_superuser, first_name, last_name, is_staff, is_active, date_joined, email, role, phone) VALUES
-- Travelers
(1,  'pbkdf2_sha256$600000$abc123$hashedpassword1==', NOW(), false, 'Alice',   'Smith',    false, true, '2024-01-10 08:00:00+00', 'alice@example.com',   'traveler', '+9779801234567'),
(2,  'pbkdf2_sha256$600000$abc123$hashedpassword2==', NOW(), false, 'Bob',     'Johnson',  false, true, '2024-01-15 09:00:00+00', 'bob@example.com',     'traveler', '+9779802345678'),
(3,  'pbkdf2_sha256$600000$abc123$hashedpassword3==', NOW(), false, 'Carol',   'Williams', false, true, '2024-02-01 10:00:00+00', 'carol@example.com',   'traveler', '+9779803456789'),
(4,  'pbkdf2_sha256$600000$abc123$hashedpassword4==', NOW(), false, 'David',   'Brown',    false, true, '2024-02-10 11:00:00+00', 'david@example.com',   'traveler', '+9779804567890'),
(5,  'pbkdf2_sha256$600000$abc123$hashedpassword5==', NOW(), false, 'Emma',    'Davis',    false, true, '2024-03-05 07:00:00+00', 'emma@example.com',    'traveler', '+9779805678901'),

-- Guides
(6,  'pbkdf2_sha256$600000$abc123$hashedpassword6==', NOW(), false, 'Hari',    'Thapa',    false, true, '2024-01-05 06:00:00+00', 'hari@example.com',    'guide',    '+9779706789012'),
(7,  'pbkdf2_sha256$600000$abc123$hashedpassword7==', NOW(), false, 'Sita',    'Rai',      false, true, '2024-01-08 06:30:00+00', 'sita@example.com',    'guide',    '+9779707890123'),
(8,  'pbkdf2_sha256$600000$abc123$hashedpassword8==', NOW(), false, 'Bikash',  'Shrestha', false, true, '2024-02-12 07:00:00+00', 'bikash@example.com',  'guide',    '+9779708901234'),

-- Hotels
(9,  'pbkdf2_sha256$600000$abc123$hashedpassword9==', NOW(), false, 'Mountain','View Hotel',false, true, '2024-01-03 05:00:00+00', 'mountainview@example.com', 'hotel', '+9771234567890'),
(10, 'pbkdf2_sha256$600000$abc123$hashedpassword10=', NOW(), false, 'Lakeside', 'Resort',  false, true, '2024-01-20 05:30:00+00', 'lakeside@example.com',     'hotel', '+9771345678901'),
(11, 'pbkdf2_sha256$600000$abc123$hashedpassword11=', NOW(), false, 'Valley',   'Inn',     false, true, '2024-02-15 06:00:00+00', 'valleyinn@example.com',    'hotel', '+9771456789012'),

-- Admin
(12, 'pbkdf2_sha256$600000$abc123$hashedpassword12=', NOW(), true,  'Admin',   'User',     true,  true, '2023-12-01 00:00:00+00', 'admin@example.com',   'admin',    '+9771567890123');

-- Reset sequence
SELECT setval('public.accounts_user_id_seq', 12);


-- ============================================================
-- 2. GUIDE PROFILES (listings_guideprofile)
-- ============================================================

INSERT INTO public.listings_guideprofile (id, bio, experience_years, languages, location, price_per_day, created_at, user_id) VALUES
(1, 'Experienced trekking guide with deep knowledge of Himalayan trails and local culture. Summited Mera Peak and Island Peak multiple times.', 8,  'Nepali, English, Hindi',         'Kathmandu, Nepal',   3500.00, '2024-01-05 06:00:00+00', 6),
(2, 'Wildlife and nature guide specializing in Chitwan and Bardia national parks. Expert in bird watching and jungle safaris.',                   5,  'Nepali, English',                'Chitwan, Nepal',     2800.00, '2024-01-08 06:30:00+00', 7),
(3, 'Cultural heritage guide focused on temples, history, and art of the Kathmandu Valley. Licensed by Nepal Tourism Board.',                    12, 'Nepali, English, French, German','Bhaktapur, Nepal',   4000.00, '2024-02-12 07:00:00+00', 8);

SELECT setval('public.listings_guideprofile_id_seq', 3);


-- ============================================================
-- 3. HOTEL PROFILES (listings_hotelprofile)
-- ============================================================

INSERT INTO public.listings_hotelprofile (id, hotel_name, description, location, contact_number, created_at, user_id) VALUES
(1, 'Mountain View Hotel',  'A cozy hotel nestled in the heart of Thamel with stunning views of the Langtang range. WiFi, hot water, rooftop restaurant.', 'Thamel, Kathmandu, Nepal',  '+9771234567890', '2024-01-03 05:00:00+00', 9),
(2, 'Lakeside Resort',      'Luxury resort on the banks of Phewa Lake, Pokhara. Kayaking, yoga, spa, and Annapurna-view rooms available.',                  'Lakeside, Pokhara, Nepal',  '+9771345678901', '2024-01-20 05:30:00+00', 10),
(3, 'Valley Inn',           'Budget-friendly guesthouse in the UNESCO heritage zone of Bhaktapur. Authentic Newari architecture, homemade food.',            'Bhaktapur, Nepal',          '+9771456789012', '2024-02-15 06:00:00+00', 11);

SELECT setval('public.listings_hotelprofile_id_seq', 3);


-- ============================================================
-- 4. ROOMS (listings_room)
-- room_type options: single, double, suite, deluxe, dormitory
-- ============================================================

INSERT INTO public.listings_room (id, room_type, price_per_night, capacity, is_available, hotel_id) VALUES
-- Mountain View Hotel
(1,  'single',    1200.00, 1, true,  1),
(2,  'double',    2000.00, 2, true,  1),
(3,  'double',    2000.00, 2, false, 1),
(4,  'suite',     4500.00, 3, true,  1),
-- Lakeside Resort
(5,  'double',    3500.00, 2, true,  2),
(6,  'deluxe',    6000.00, 2, true,  2),
(7,  'suite',     9500.00, 4, true,  2),
(8,  'single',    2500.00, 1, false, 2),
-- Valley Inn
(9,  'single',     800.00, 1, true,  3),
(10, 'double',    1400.00, 2, true,  3),
(11, 'dormitory',  500.00, 6, true,  3);

SELECT setval('public.listings_room_id_seq', 11);


-- ============================================================
-- 5. TOUR PACKAGES (listings_package)
-- ============================================================

INSERT INTO public.listings_package (id, title, description, price, duration_days, location, created_at, guide_id) VALUES
(1, 'Everest Base Camp Trek',        'Classic 14-day EBC trek via Namche Bazaar, Tengboche, and Gorakshep. All permits and teahouse accommodation included.', 45000.00, 14, 'Solukhumbu, Nepal',       '2024-01-06 07:00:00+00', 1),
(2, 'Annapurna Circuit',             '18-day circuit covering Thorong La pass at 5416m. Stunning diversity from sub-tropical to alpine.',                     55000.00, 18, 'Annapurna Region, Nepal', '2024-01-06 08:00:00+00', 1),
(3, 'Chitwan Jungle Safari',         '3-day wildlife safari including elephant bathing, canoe rides, tharu cultural show, and jeep safari.',                  12000.00,  3, 'Chitwan, Nepal',          '2024-01-09 07:00:00+00', 2),
(4, 'Bardia Tiger Reserve Tour',     '5-day tour to spot Royal Bengal Tigers, one-horned rhinos, and gharials in the wild western jungle.',                   22000.00,  5, 'Bardia, Nepal',           '2024-01-09 08:00:00+00', 2),
(5, 'Kathmandu Heritage Walk',       '1-day guided walk through Pashupatinath, Boudhanath, Swayambhunath, and Patan Durbar Square.',                          3500.00,   1, 'Kathmandu Valley, Nepal', '2024-02-13 07:00:00+00', 3),
(6, 'Bhaktapur & Panauti Day Tour',  'Full-day cultural immersion in two ancient Newari towns. Includes traditional pottery workshop and lunch.',              4200.00,   1, 'Bhaktapur & Panauti',     '2024-02-13 08:00:00+00', 3);

SELECT setval('public.listings_package_id_seq', 6);


-- ============================================================
-- 6. ROOM BOOKINGS (booking_roombooking)
-- status options: pending, confirmed, cancelled, completed
-- ============================================================

INSERT INTO public.booking_roombooking (id, check_in, check_out, status, created_at, room_id, traveler_id) VALUES
(1, '2024-05-01', '2024-05-05', 'completed',  '2024-04-10 10:00:00+00', 2,  1),
(2, '2024-05-10', '2024-05-12', 'completed',  '2024-04-20 11:00:00+00', 5,  2),
(3, '2024-06-01', '2024-06-03', 'confirmed',  '2024-05-15 09:00:00+00', 6,  3),
(4, '2024-06-15', '2024-06-20', 'confirmed',  '2024-05-20 10:00:00+00', 7,  4),
(5, '2024-07-01', '2024-07-02', 'pending',    '2024-06-01 08:00:00+00', 10, 5),
(6, '2024-07-10', '2024-07-15', 'cancelled',  '2024-06-10 09:00:00+00', 4,  1),
(7, '2024-08-01', '2024-08-04', 'confirmed',  '2024-07-01 07:00:00+00', 9,  2),
(8, '2024-08-20', '2024-08-22', 'pending',    '2024-07-25 10:00:00+00', 1,  3);

SELECT setval('public.booking_roombooking_id_seq', 8);


-- ============================================================
-- 7. PACKAGE BOOKINGS (booking_packagebooking)
-- ============================================================

INSERT INTO public.booking_packagebooking (id, start_date, status, created_at, package_id, traveler_id) VALUES
(1, '2024-05-10', 'completed', '2024-04-15 08:00:00+00', 1, 1),
(2, '2024-05-20', 'completed', '2024-04-25 09:00:00+00', 3, 2),
(3, '2024-06-05', 'confirmed', '2024-05-10 10:00:00+00', 5, 3),
(4, '2024-06-20', 'confirmed', '2024-05-25 11:00:00+00', 2, 4),
(5, '2024-07-01', 'pending',   '2024-06-05 08:00:00+00', 4, 5),
(6, '2024-07-15', 'cancelled', '2024-06-15 09:00:00+00', 6, 1),
(7, '2024-08-10', 'confirmed', '2024-07-10 10:00:00+00', 1, 2);

SELECT setval('public.booking_packagebooking_id_seq', 7);


-- ============================================================
-- 8. HOTEL REVIEWS (reviews_hotelreview)
-- ============================================================

INSERT INTO public.reviews_hotelreview (id, rating, comment, created_at, hotel_id, traveler_id) VALUES
(1, 5, 'Fantastic stay! The staff was incredibly helpful and the mountain views from the rooftop were breathtaking. Will definitely come back.', '2024-05-06 12:00:00+00', 1, 1),
(2, 4, 'Great location in Thamel, easy to get around. Room was clean, hot water was consistent. Only minor issue was street noise at night.',    '2024-05-13 13:00:00+00', 2, 2),
(3, 5, 'Lakeside Resort exceeded all expectations. The lake-view room was gorgeous and kayaking at sunrise was unforgettable.',                  '2024-06-04 14:00:00+00', 2, 3),
(4, 4, 'Valley Inn is a hidden gem. Loved the authentic Newari feel and the homemade sel roti for breakfast!',                                  '2024-07-03 10:00:00+00', 3, 2),
(5, 3, 'Decent place for the price. Bathroom could use an upgrade but the location near Bhaktapur Durbar Square is unbeatable.',                 '2024-07-05 11:00:00+00', 3, 5);

SELECT setval('public.reviews_hotelreview_id_seq', 5);


-- ============================================================
-- 9. GUIDE REVIEWS (reviews_guidereview)
-- ============================================================

INSERT INTO public.reviews_guidereview (id, rating, comment, created_at, guide_id, traveler_id) VALUES
(1, 5, 'Hari made our EBC trek a life-changing experience. His knowledge of the mountains, local culture, and first aid skills gave us complete confidence.', '2024-05-25 12:00:00+00', 1, 1),
(2, 5, 'Sita is a wildlife encyclopedia! She spotted a Bengal Tiger on day 2 and knew every bird call in the jungle. Highly recommend for Chitwan.',          '2024-06-01 13:00:00+00', 2, 2),
(3, 4, 'Bikash''s knowledge of Kathmandu Valley history is outstanding. The heritage walk felt like a university lecture, in the best possible way.',          '2024-06-08 14:00:00+00', 3, 3),
(4, 5, 'Best trekking guide we''ve ever had. Hari knew exactly when to push and when to rest. Arrived at EBC healthy and happy!',                             '2024-08-25 10:00:00+00', 1, 4);

SELECT setval('public.reviews_guidereview_id_seq', 4);


-- ============================================================
-- 10. CHAT CONVERSATIONS (chat_conversation)
-- ============================================================

INSERT INTO public.chat_conversation (id, created_at, updated_at, hotel_id, user_id) VALUES
(1, '2024-04-08 09:00:00+00', '2024-04-10 15:00:00+00', 1, 1),
(2, '2024-04-18 10:00:00+00', '2024-04-20 12:00:00+00', 2, 2),
(3, '2024-05-13 08:00:00+00', '2024-05-14 09:00:00+00', 2, 3),
(4, '2024-06-28 11:00:00+00', '2024-06-29 10:00:00+00', 3, 5);

SELECT setval('public.chat_conversation_id_seq', 4);


-- ============================================================
-- 11. CHAT MESSAGES (chat_message)
-- ============================================================

INSERT INTO public.chat_message (id, content, created_at, is_read, read_at, conversation_id, sender_id) VALUES
-- Conversation 1: Alice ↔ Mountain View Hotel
(1,  'Hello! I''d like to book a double room from May 1–5. Is it available?',                          '2024-04-08 09:00:00+00', true,  '2024-04-08 09:30:00+00', 1, 1),
(2,  'Hi Alice! Yes, Room 2 (double) is available for those dates. Shall I confirm the booking?',      '2024-04-08 09:30:00+00', true,  '2024-04-08 10:00:00+00', 1, 9),
(3,  'Yes please! Also does the rate include breakfast?',                                              '2024-04-08 10:00:00+00', true,  '2024-04-09 08:00:00+00', 1, 1),
(4,  'Breakfast is an additional NPR 350 per person per day. I''ve confirmed your booking!',           '2024-04-09 08:00:00+00', true,  '2024-04-10 15:00:00+00', 1, 9),
-- Conversation 2: Bob ↔ Lakeside Resort
(5,  'Do you have availability for 2 nights from May 10?',                                            '2024-04-18 10:00:00+00', true,  '2024-04-18 11:00:00+00', 2, 2),
(6,  'Hello Bob! We have our standard double and deluxe lake-view rooms available. Which do you prefer?','2024-04-18 11:00:00+00', true, '2024-04-18 12:00:00+00', 2, 10),
(7,  'I''ll take the standard double please.',                                                         '2024-04-18 12:00:00+00', true,  '2024-04-20 12:00:00+00', 2, 2),
-- Conversation 3: Carol ↔ Lakeside Resort
(8,  'Hi, is the Annapurna view suite available in June?',                                            '2024-05-13 08:00:00+00', true,  '2024-05-13 09:00:00+00', 3, 3),
(9,  'Yes Carol! The suite is available June 1–3. It includes a private balcony with mountain views.', '2024-05-13 09:00:00+00', false, NULL,                    3, 10),
-- Conversation 4: Emma ↔ Valley Inn
(10, 'Is your dormitory suitable for solo female travelers?',                                         '2024-06-28 11:00:00+00', true,  '2024-06-28 12:00:00+00', 4, 5),
(11, 'Absolutely Emma! We have a female-only dorm section. Very safe and social environment.',         '2024-06-28 12:00:00+00', false, NULL,                    4, 11);

SELECT setval('public.chat_message_id_seq', 11);


-- ============================================================
-- 12. NOTIFICATIONS (notifications_notification)
-- notification_type: booking, review, message, system
-- ============================================================

INSERT INTO public.notifications_notification (id, notification_type, title, message, is_read, created_at, recipient_id, related_object_id) VALUES
(1,  'booking',  'Booking Confirmed',        'Your room booking at Mountain View Hotel (May 1–5) has been confirmed.',       true,  '2024-04-09 08:30:00+00', 1,  1),
(2,  'booking',  'Booking Confirmed',        'Your room booking at Lakeside Resort (May 10–12) has been confirmed.',         true,  '2024-04-19 09:00:00+00', 2,  2),
(3,  'booking',  'New Booking Received',     'You have a new room booking from Carol Williams for June 1–3.',                false, '2024-05-15 09:30:00+00', 10, 3),
(4,  'booking',  'Package Booking Confirmed','Your Everest Base Camp Trek booking starting May 10 is confirmed.',            true,  '2024-04-16 10:00:00+00', 1,  1),
(5,  'booking',  'Booking Cancelled',        'Your Bhaktapur & Panauti Day Tour booking has been cancelled as requested.',   true,  '2024-06-16 09:00:00+00', 1,  6),
(6,  'review',   'New Review Received',      'Alice Smith left a 5-star review for Mountain View Hotel.',                    true,  '2024-05-06 12:30:00+00', 9,  1),
(7,  'review',   'New Review Received',      'You received a 5-star review from Alice Smith for the EBC Trek package.',      false, '2024-05-26 12:30:00+00', 6,  1),
(8,  'message',  'New Message',              'You have a new message from Alice Smith.',                                     true,  '2024-04-08 09:05:00+00', 9,  1),
(9,  'message',  'New Message',              'Mountain View Hotel replied to your inquiry.',                                 true,  '2024-04-08 09:35:00+00', 1,  2),
(10, 'system',   'Welcome to TravelNepal!',  'Your account has been verified. Start exploring packages and hotels.',         true,  '2024-01-10 08:05:00+00', 1,  NULL),
(11, 'system',   'Profile Approved',         'Your guide profile has been approved. You can now list packages.',             true,  '2024-01-06 07:00:00+00', 6,  NULL),
(12, 'booking',  'New Package Booking',      'David Brown booked your Annapurna Circuit package starting June 20.',          false, '2024-05-25 11:30:00+00', 6,  4);

SELECT setval('public.notifications_notification_id_seq', 12);


COMMIT;

-- ============================================================
-- QUICK VERIFICATION QUERIES
-- ============================================================

-- Uncomment to verify after inserting:
-- SELECT role, COUNT(*) FROM public.accounts_user GROUP BY role;
-- SELECT COUNT(*) AS rooms FROM public.listings_room;
-- SELECT COUNT(*) AS packages FROM public.listings_package;
-- SELECT COUNT(*) AS room_bookings FROM public.booking_roombooking;
-- SELECT COUNT(*) AS package_bookings FROM public.booking_packagebooking;
-- SELECT COUNT(*) AS messages FROM public.chat_message;
