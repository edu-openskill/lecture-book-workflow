package com.metacoding.delivery.adapter.message;

public record DeliveryCreatedEvent(int orderId, int deliveryId, boolean isSuccess) {}
